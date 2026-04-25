from functions.Initializations.llm_init import llm
from langchain.agents import create_agent


# ---------------------------
# DRAFTING AGENT (UNCHANGED)
# ---------------------------
drafting_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="""
                You are a Regulatory Medical Writing System.

                You generate and refine regulatory documents strictly based on the provided context derived from:
                - ICH E6(R3)
                - ICH E3
                - ICH E8(R1)
                - FDA Real-World Evidence (RWE) guidance

                SYSTEM CONSTRAINTS (MANDATORY):
                1. Use ONLY the provided context. Do NOT use external knowledge.
                2. Do NOT infer, assume, or fabricate any information.
                3. If required information is missing, explicitly state: "Information not provided."
                4. Do NOT produce conversational or chatbot-style responses.
                5. Output must be formal, structured, and regulatory in tone.
                6. Maintain consistency with previous drafts unless corrections require changes.
                7. Apply corrections precisely without altering unrelated sections.

                ---

                TASK MODES:

                ### MODE 1: INITIAL DRAFT
                If no prior draft is provided:
                - Generate a structured regulatory document based on the input.

                ### MODE 2: REFINEMENT
                If a previous draft and corrections are provided:
                - Revise the document by applying ONLY the given corrections
                - Do NOT introduce new content beyond corrections
                - Preserve all compliant sections unchanged

                ---

                STRUCTURE REQUIREMENTS (ICH E3-aligned):

                - Title
                - Synopsis
                - Introduction
                - Objectives
                - Study Design (align with ICH E8(R1) if context supports)
                - Methodology
                - Statistical Considerations (only if present)
                - Results (only if data provided)
                - Safety / Adverse Events (align with ICH E6(R3) if present)
                - Discussion
                - Conclusion

                ---

                CONTENT RULES:

                - Each section must contain ONLY information supported by context
                - If insufficient data → write: "Information not provided."
                - Do NOT merge or skip sections unless explicitly justified by context
                - Maintain clarity, precision, and professional regulatory language
                - Avoid redundancy and filler text

                ---

                COMPLIANCE ALIGNMENT:

                - Reflect ICH E6(R3): safety, data integrity, compliance principles
                - Reflect ICH E8(R1): study design logic (if present)
                - Reflect FDA RWE: only if explicitly supported in context

                ---

                INPUTS:

                CONTEXT:
                {context}

                USER INPUT:
                {input}

                PREVIOUS DRAFT (optional):
                {draft}

                CORRECTIONS (optional):
                {corrections}

                ---

                OUTPUT FORMAT:

                Return ONLY the structured regulatory document.

                Do NOT include explanations, reasoning, or commentary.
            """
)

def extract_answer(response):
    """
    Handles LangChain agent + dict + message formats safely
    """

    if response is None:
        return "No response generated."

    # Case 1: Agent-style response
    if isinstance(response, dict):
        if "messages" in response and len(response["messages"]) > 0:
            msg = response["messages"][-1]
            return getattr(msg, "content", str(msg))

        return response.get("answer") or response.get("output") or str(response)

    # Case 2: Direct LangChain message
    return getattr(response, "content", str(response))


def drafting_pipeline(query, retriever, drafting_agent):
    print(f"Processing drafting request: {query}")

    # ---------------------------
    # STEP 1: Retrieve context
    # ---------------------------
    results = retriever.retrieve(query, top_k=5)

    print(f"Retrieved {len(results)} documents")

    # HARD GUARD (important fix)
    if not results or len(results) == 0:
        return {
            "answer": "No relevant regulatory context found to generate a reliable draft.",
            "sources": [],
            "confidence_score": 0.0,
            "warning": "No retrieval results"
        }

    # Optional: filter weak matches
    print("Retrieved scores:")

    for r in results:
        print(r.get("similarity_score", 0))

    if len(results) == 0:
        return {
            "answer": "Retrieved documents were not relevant enough to generate a reliable draft.",
            "sources": [],
            "confidence_score": 0.0,
            "warning": "Low relevance retrieval"
        }

    # ---------------------------
    # STEP 2: Build context
    # ---------------------------
    context = "\n\n---\n\n".join(
        f"[Source: {doc.get('metadata', {}).get('source_file', 'unknown')}]\n{doc.get('content', '')}"
        for doc in results
    )

    sources = [
        {
            "source": doc.get("metadata", {}).get("source_file", "unknown"),
            "page": doc.get("metadata", {}).get("page", "unknown"),
            "score": doc.get("similarity_score", 0.0)
        }
        for doc in results
    ]

    confidence_score = (
        max(doc.get("similarity_score", 0.0) for doc in results)
    )

    # ---------------------------
    # STEP 3: Call LLM agent
    # ---------------------------
    try:
        response = drafting_agent.invoke({
            "context": context,
            "input": query
        })

        return {
            "answer": extract_answer(response),
            "sources": sources,
            "confidence_score": confidence_score,
            "warning": (
                "Potential Regulatory Risk Identified"
                if confidence_score < 0.45
                else None
            )
        }

    except Exception as e:
        return {
            "answer": f"Error generating draft: {str(e)}",
            "sources": sources,
            "confidence_score": confidence_score,
            "warning": "Generation failure"
        }