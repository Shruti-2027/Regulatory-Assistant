from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from functions.agents.drafting import drafting_agent
from functions.agents.validating import validating_agent
from functions.agent_workflow.Generating_draft import generate_draft_session
from functions.agent_workflow.ValidatingDraftSendingResponse import validate_and_prepare_revision
from functions.agent_workflow.ResolveFeedback import revise_draft_from_validation
from functions.final_output import export_to_pdf, clean_markdown
from initializations import build_rag_system


# ----------------------------
# FastAPI App
# ----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# 📁 CREATE + MOUNT PDF FOLDER
# ----------------------------
PDF_DIR = "generated_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

app.mount("/files", StaticFiles(directory=PDF_DIR), name="files")


# ----------------------------
# Global initialization
# ----------------------------
rag_retriever = None


@app.on_event("startup")
def startup_event():
    global rag_retriever
    rag_retriever = build_rag_system()


# ----------------------------
# Request Models
# ----------------------------
class DraftRequest(BaseModel):
    query: str


class ValidateRequest(BaseModel):
    draft_session: dict


class ReviseRequest(BaseModel):
    draft_session: dict
    validation_result: dict


class ExportRequest(BaseModel):
    final_revision: dict


# ----------------------------
# 1. Draft Endpoint
# ----------------------------
@app.post("/draft")
def create_draft(request: DraftRequest):
    draft_session = generate_draft_session(
        user_query=request.query,
        retriever=rag_retriever,
        drafting_agent=drafting_agent
    )
    return draft_session


# ----------------------------
# 2. Validation Endpoint
# ----------------------------
@app.post("/validate")
def validate(request: ValidateRequest):
    draft_session = request.draft_session

    validation_result = validate_and_prepare_revision(
        config_id=draft_session["config_id"],
        original_query=draft_session["original_query"],
        draft_output=draft_session["draft_output"],
        validation_input=draft_session["validation_input"],
        validation_agent=validating_agent
    )

    return validation_result


# ----------------------------
# 3. Revise Endpoint
# ----------------------------
@app.post("/revise")
def revise(request: ReviseRequest):
    draft_session = request.draft_session
    validation_result = request.validation_result

    final_revision = revise_draft_from_validation(
        config_id=draft_session["config_id"],
        original_query=draft_session["original_query"],
        previous_draft=draft_session["draft_output"],
        validation_feedback=validation_result["validation_feedback"],
        retriever=rag_retriever,
        drafting_agent=drafting_agent
    )

    return final_revision


# ----------------------------
# 4. Export PDF Endpoint (FIXED)
# ----------------------------
@app.post("/export")
def export(request: ExportRequest):
    final_revision = request.final_revision

    clean_text = clean_markdown(final_revision["improved_draft"])
    config_id = final_revision["config_id"]

    filename = f"CSR_Report_{config_id}.pdf"
    file_path = os.path.join(PDF_DIR, filename)

    # ✅ NOW PASS CORRECT PATH
    export_to_pdf(
        config_id=config_id,
        improved_draft=clean_text,
        output_path=file_path
    )

    return {
        "pdf_file": f"http://127.0.0.1:8000/files/{filename}"
    }