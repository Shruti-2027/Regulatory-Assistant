import uuid
from functions.agents.drafting import drafting_pipeline


def generate_draft_session(
    user_query,
    retriever,
    drafting_agent
):
    """
    Handles:
    - draft generation
    - config/thread ID creation
    - preparing output for validation pipeline

    Returns:
    {
        "config_id": str,
        "original_query": str,
        "draft_output": str,
        "validation_input": str,
        "sources": list,
        "confidence": float
    }
    """

    print(f"Starting drafting session for: {user_query}")

    # Step 1: Generate unique config/thread ID
    config_id = str(uuid.uuid4())

    # Step 2: Call drafting pipeline
    draft_result = drafting_pipeline(
        query=user_query,
        retriever=retriever,
        drafting_agent=drafting_agent
    )

    draft_output = draft_result["answer"]
    sources = draft_result.get("sources", [])
    confidence = draft_result.get("confidence", 0.0)

    # Step 3: Prepare validation-ready input
    validation_input = f"""
        Please validate the following Clinical Study Report draft
        for ICH E3 compliance, completeness, formatting issues,
        missing sections, and regulatory inconsistencies.

        Original User Request:
        {user_query}

        Generated Draft:
        {draft_output}

        Return only:
        - issues found
        - missing sections
        - correction instructions

        Do NOT rewrite the draft.
        """

    # Step 4: Return structured response
    return {
        "config_id": config_id,
        "original_query": user_query,
        "draft_output": draft_output,
        "validation_input": validation_input,
        "sources": sources,
        "confidence": confidence
    }