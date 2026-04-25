from functions.agents.drafting import drafting_agent
from functions.agents.validating import validating_agent
from functions.agent_workflow.Generating_draft import generate_draft_session
from functions.agent_workflow.ValidatingDraftSendingResponse import validate_and_prepare_revision
from functions.agent_workflow.ResolveFeedback import revise_draft_from_validation
from functions.final_output import export_to_pdf
from functions.final_output import clean_markdown
from initializations import build_rag_system
from fastapi import FastAPI
app = FastAPI()

def main():

    rag_retriever = build_rag_system()
   # Drafting test
    draft_session = generate_draft_session(
    user_query="Write a CSR synopsis for a Phase 3 oncology study",
    retriever=rag_retriever,
    drafting_agent=drafting_agent
    )

    print(draft_session)


    # Validation
    validation_result = validate_and_prepare_revision(
    config_id=draft_session["config_id"],
    original_query=draft_session["original_query"],
    draft_output=draft_session["draft_output"],
    validation_input=draft_session["validation_input"],
    validation_agent=validating_agent
    )

    print(validation_result)

    # Resolve feedback
    final_revision = revise_draft_from_validation(
    config_id=draft_session["config_id"],
    original_query=draft_session["original_query"],
    previous_draft=draft_session["draft_output"],
    validation_feedback=validation_result["validation_feedback"],
    retriever=rag_retriever,
    drafting_agent=drafting_agent
    )

    print(final_revision)

    # Final output
    clean_text = clean_markdown(final_revision["improved_draft"])

    pdf_file = export_to_pdf(
        config_id=final_revision["config_id"],
        improved_draft=clean_text
    )


if __name__ == "__main__":
    main()