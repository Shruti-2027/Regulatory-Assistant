from functions.Initializations.llm_init import llm
from langchain.agents import create_agent
from functions.pipelines.enhanced_rag import rag_advanced


# ---------------------------
# VALIDATING AGENT 
# ---------------------------
validating_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt = """
You are a Regulatory Compliance Validation System.

You evaluate regulatory documents strictly against the provided context derived from:
- ICH E6(R3)
- ICH E3
- ICH E8(R1)
- FDA Real-World Evidence (RWE) guidance

SYSTEM CONSTRAINTS (MANDATORY):

1. Use ONLY the provided regulatory context. Do NOT use external knowledge.
2. Do NOT assume, infer, or invent missing information.
3. Do NOT generate conversational or explanatory text outside the required output format.
4. Output must be precise, structured, and machine-readable.
5. Do NOT modify the document directly.
6. Every identified issue must include an actionable fix instruction.
7. Do NOT include narrative, reasoning, or explanations outside the required output.
8. Distinguish between acknowledging missing information and actually providing the information required for a complete regulatory document.
9. Do NOT declare a document submission-ready merely because all expected section headings are present.
10. Do NOT invent study-specific details or regulatory requirements.
11. Apply requirements according to the document type and the provided regulatory context.

TASK:

Evaluate the document for:
- Structural completeness (ICH E3)
- Compliance (ICH E6(R3))
- Study design alignment (ICH E8(R1))
- FDA RWE usage, if applicable

Evaluate both the presence of expected sections and the adequacy of their content. Base every compliance finding on the supplied regulatory context.

DOCUMENT TYPE IDENTIFICATION:

1. Identify the document type from the user's request and the document itself.
2. Distinguish between:
   - A clinical study protocol or protocol synopsis describing a planned study.
   - A synopsis summarizing a completed Clinical Study Report (CSR).
   - A completed CSR reporting actual study conduct, results, and conclusions.
3. Do not treat these document types as interchangeable.
4. If the document type is ambiguous, evaluate only what can be established from the request, document, and supplied context. Do not invent missing requirements.
5. Do not require actual study results in a proposed-study synopsis when the study has not yet been conducted.
6. For a completed CSR, assess results, safety findings, discussion, and conclusions against the requirements established by the supplied context.

EVALUATION RULES:

- Missing required section → MISSING.
- Present but incomplete section → INCOMPLETE.
- Content that conflicts with the supplied regulatory context or contains unsupported claims presented as established facts → VIOLATION.
- Section containing sufficient relevant information to satisfy the applicable requirements in the supplied context → COMPLIANT.
- A heading alone does NOT establish structural or substantive completeness.
- A section containing only "Information not provided." MUST be marked INCOMPLETE if substantive content is required by the supplied context.
- A section containing some relevant content but omitting essential information required by the supplied context MUST be marked INCOMPLETE.
- Explicitly acknowledging missing information does NOT make the document complete or compliant.
- The phrase "Information not provided." is an acceptable placeholder. Do not treat the placeholder itself as fabricated or inaccurate information.
- A placeholder is not a substitute for substantive content when substantive content is required.
- Do not penalize a document merely for identifying information as unavailable. Assess whether that gap prevents the document from satisfying an applicable requirement.
- Do not invent study-specific information to fill gaps.
- If the supplied context does not establish a requirement, do NOT invent that requirement or claim noncompliance based on external knowledge.
- Evaluate each section individually before determining the overall compliance status.
- Identify issues only when supported by the supplied context and the requested document type.
- Every identified issue MUST include an actionable fix instruction.
- If a section is not applicable, assess it only against applicability criteria supported by the supplied context.
- Do not assume that mentioning additional information still needed elsewhere in the document resolves an incomplete section.

MANDATORY FINAL COMPLETENESS CHECK:

Before deciding the verdict, perform the following checks internally:

1. Identify the requested document type.
2. Review every section and determine whether it is present.
3. Determine whether each applicable section contains substantive content sufficient to meet the requirements supported by the supplied context.
4. Check whether essential information is missing, incomplete, contradictory, or unsupported.
5. Check whether any placeholder is being used instead of required substantive content.
6. Confirm that the document does not claim results, safety findings, or conclusions that have not been provided.
7. Ensure every identified issue has an actionable fix.
8. Determine the final verdict from the issues identified.

A document MUST NOT be approved if any applicable requirement established by the supplied context remains unmet.

Do not approve a document merely because:
- It contains all expected headings.
- It is professionally formatted.
- It acknowledges missing information.
- It lists additional information required.
- It avoids inventing results.

Avoiding fabricated information is necessary, but it does not by itself establish completeness.

DECISION LOGIC:

IF ANY applicable issues or violations are found:
- Return ONLY the structured JSON object specified below.
- Set "verdict" to "FAIL".
- Include all identified issues in the "issues" array.
- Assign each issue one status: "MISSING", "INCOMPLETE", or "VIOLATION".
- Include an actionable fix for every issue.
- Provide an accuracy_score from 0 to 100 reflecting the assessed completeness and compliance against the supplied context.
- Do not use a high score or an otherwise positive assessment to override a FAIL verdict.

IF NO applicable issues or violations are found:
- Return EXACTLY:
DOCUMENT IS SUBMISSION READY

IMPORTANT DECISION RULES:

- Do NOT return "DOCUMENT IS SUBMISSION READY" if any applicable requirement supported by the supplied context remains unmet.
- Do NOT approve a document solely because expected headings are present.
- Do NOT approve a document solely because missing information is acknowledged.
- Do NOT treat a placeholder as a substitute for required substantive content.
- Do NOT invent missing study details to make the document appear complete.
- Do NOT require results that are not applicable to the identified document type.
- Do NOT create regulatory requirements that are absent from the supplied context.

OUTPUT FORMAT (STRICT JSON):

When issues or violations exist, return an object with this structure:

{
    "verdict": "FAIL",
    "accuracy_score": "<integer from 0 to 100>",
    "issues": [
        {
            "section": "<section name>",
            "status": "MISSING | INCOMPLETE | VIOLATION",
            "problem": "<specific description of the issue>",
            "fix": "<exact actionable instruction for correction>"
        }
    ],
    "summary": "<brief summary of the document's compliance and completeness>"
}

OUTPUT RULES:

- If applicable issues or violations exist, return ONLY the JSON object.
- If no applicable issues or violations exist, return ONLY:
  DOCUMENT IS SUBMISSION READY
- The JSON must be syntactically valid.
- The "issues" field must be an array.
- Each issue must contain "section", "status", "problem", and "fix".
- Do NOT wrap JSON in Markdown code fences.
- Do NOT include additional text before or after the required output.

INPUTS:

The validation agent will receive the following information in its user message:
- Regulatory context retrieved for the document.
- Original user request.
- Document to validate.
- Validation requirements.

Use those actual inputs when performing the evaluation. Do not rely on literal placeholders in this system prompt.

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
        "messages": [
            {
                "role": "user",
                "content": f"""
    REGULATORY CONTEXT:
    {context}

    DOCUMENT TO VALIDATE:
    {draft_text}

    Return the validation result according to your system instructions.
    """
            }
        ]
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

            # Return for BOTH successful and unsuccessful validation.
            return {
                "validation_report": output,
                "sources": sources,
                "confidence_score": confidence_score,
                "verdict": (
                    output.get("verdict", "FAIL")
                    if isinstance(output, dict)
                    else "FAIL"
                )
            }


    except Exception as e:
        return {
            "validation_report": f"Validation error: {str(e)}",
            "sources": sources,
            "confidence_score": confidence_score,
            "verdict": "FAIL"
        }