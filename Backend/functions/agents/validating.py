from functions.Initializations.llm_init import llm
from langchain.agents import create_agent
from functions.pipelines.enhanced_rag import rag_advanced


# ---------------------------
# VALIDATING AGENT 
# ---------------------------
validating_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt= """
                You are a Regulatory Compliance Validation System.

                You evaluate regulatory documents strictly against the provided context derived from:
                - ICH E6(R3)
                - ICH E3
                - ICH E8(R1)
                - FDA Real-World Evidence (RWE) guidance

                ---

                SYSTEM CONSTRAINTS (MANDATORY):
                1. Use ONLY the provided context. Do NOT use external knowledge.
                2. Do NOT assume or infer missing information.
                3. Do NOT generate conversational or explanatory text.
                4. Output must be precise, structured, and machine-readable.
                5. Do NOT modify the document directly.
                6. Every issue must include an actionable fix instruction.
                7. Do NOT include any narrative, reasoning, or explanation outside output format.

                ---

                TASK:
                Evaluate the document for:
                - Structural completeness (ICH E3)
                - Compliance (ICH E6(R3))
                - Study design alignment (ICH E8(R1))
                - FDA RWE usage (if applicable)

                ---

                EVALUATION RULES:
                - Missing section → Violation
                - Incomplete section → Issue
                - Proper section → Compliant
                - If "Information not provided." is used correctly → DO NOT flag as issue

                ---

                DECISION LOGIC:

                IF ANY issues or violations are found:
                → Return structured validation output (see format below)

                IF NO issues or violations:
                → Return EXACT STRING:
                DOCUMENT IS SUBMISSION READY

                ---

                OUTPUT FORMAT (STRICT JSON STYLE):

                {
                "verdict": "PASS" | "FAIL",
                "accuracy_score": "<0-100>",
                "issues": [
                    {
                    "section": "<section name>",
                    "status": "MISSING | INCOMPLETE | VIOLATION",
                    "problem": "<what is wrong>",
                    "fix": "<exact actionable instruction for correction>"
                    }
                ],
                "summary": "brief structured summary of compliance state"
                }

                ---

                INPUTS:

                CONTEXT:
                {context}

                DOCUMENT:
                {draft}

                ---

                OUTPUT RULES:
                - If issues exist → return ONLY JSON object
                - If no issues → return ONLY:
                DOCUMENT IS SUBMISSION READY
        """
             
)

# ---------------------------
# RAG ADVANCED PIPELINE USAGE
# ---------------------------
def validation_pipeline(draft_text, retriever, validating_agent, top_k=5, min_score=0.25):
    """
    Validation RAG Pipeline:
    - Retrieves same context as drafting
    - Compares draft vs documents
    - Produces strict audit report
    """

    print("Running validation pipeline...")

    # ---------------------------
    # STEP 1: USE ADVANCED RAG
    # ---------------------------
    rag_result = rag_advanced(
        query=draft_text,
        retriever=retriever,
        llm = llm,
        top_k=top_k,
        min_score=min_score,
        return_context=True
    )

    context = rag_result.get("context" , "")
    sources_raw = rag_result.get("sources", [])
    confidence_score = rag_result.get("confidence_score" , 0.0)

    # ---------------------------
    # STEP 2: LOW CONTEXT SAFETY
    # ---------------------------
    if confidence_score == 0.0 or not context:
        return {
            "validation_report": "Cannot validate due to insufficient context.",
            "sources": [],
            "confidence_score": 0.0,
            "verdict": "FAIL"
        }

    sources = list(set([doc["source"] for doc in sources_raw]))

    # ---------------------------
# STEP 3: RUN VALIDATION
# ---------------------------
    try:
        response = validating_agent.invoke({
            "context": context,
            "draft": draft_text
        })

        # ---------------------------
        # STEP 4: NORMALIZED OUTPUT HANDLING
        # ---------------------------

        output = None

        # Case 1: dict response (AgentExecutor style)
        if isinstance(response, dict):

            if "messages" in response and response["messages"]:
                output = getattr(response["messages"][-1], "content", str(response["messages"][-1]))

            elif "output" in response:
                output = response["output"]

            elif "content" in response:
                output = response["content"]

            else:
                output = str(response)

        # Case 2: direct LLM / AIMessage
        else:
            output = getattr(response, "content", str(response))

        # ---------------------------
        # OPTIONAL: CLEAN SUCCESS STRING
        # ---------------------------
        if isinstance(output, str) and "DOCUMENT IS SUBMISSION READY" in output:
            output = {
                "verdict": "PASS",
                "summary": "Document is submission ready"
            }

            return {
                "validation_report": output,
                "sources": sources,
                "confidence_score": confidence_score,
                "verdict": "UNKNOWN" 
            }

    except Exception as e:
        return {
            "validation_report": f"Validation error: {str(e)}",
            "sources": sources,
            "confidence_score": confidence_score,
            "verdict": "FAIL"
        }