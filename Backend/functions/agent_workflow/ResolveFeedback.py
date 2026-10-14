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
- Fix the identified issues that can be resolved using available information.
- Maintain an appropriate regulatory writing style.
- Preserve valid existing sections and accurate information.
- Do not invent study facts, procedures, dosing regimens, sample-size
  justifications, statistical analysis plan details, or study results.
- Do not claim that an appendix, protocol, or analysis plan exists
  unless its contents were actually provided.
- If information is missing, state "Not provided" or list it under
  "Additional Information Required."
- If you suggest a procedure or method not specified in the source,
  clearly label it as a proposal requiring confirmation.
- Distinguish a hypothetical study protocol synopsis from a completed
  Clinical Study Report. Do not invent efficacy or safety findings.
- Do not claim ICH compliance or submission readiness solely because
  the document contains the expected headings.

Generate the improved final draft.
"""


    # Step 2: Send to drafting pipeline
    revised_result = drafting_pipeline(
        query=revision_query,
        retriever=retriever,
        drafting_agent=drafting_agent,
        retrieval_query=original_query
    )

    improved_draft = revised_result["answer"]

    return {
        "config_id": config_id,
        "improved_draft": improved_draft,
        "status": "revised"
    }