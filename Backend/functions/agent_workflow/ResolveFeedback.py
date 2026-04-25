from functions.agents.drafting import drafting_pipeline

def revise_draft_from_validation(
    config_id,
    original_query,
    previous_draft,
    validation_feedback,
    retriever,
    drafting_agent
):
    """
    Takes validation feedback and sends it back to the drafting agent
    to generate an improved draft.

    Returns:
    {
        "config_id": str,
        "improved_draft": str,
        "status": str
    }
    """

    print(f"Revising draft for config_id: {config_id}")

    # Step 1: Prepare revision prompt
    revision_query = f"""
Please improve the previous Clinical Study Report (CSR) draft
based on the validation feedback below.

Original User Request:
{original_query}

Previous Draft:
{previous_draft}

Validation Feedback:
{validation_feedback}

Instructions:
- Fix all identified issues
- Maintain ICH E3 compliance
- Keep professional regulatory writing style
- Do not remove valid existing sections
- Improve completeness and accuracy

Generate the improved final draft.
"""

    # Step 2: Send to drafting pipeline
    revised_result = drafting_pipeline(
        query=revision_query,
        retriever=retriever,
        drafting_agent=drafting_agent
    )

    improved_draft = revised_result["answer"]

    return {
        "config_id": config_id,
        "improved_draft": improved_draft,
        "status": "revised"
    }