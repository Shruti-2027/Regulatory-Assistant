def validate_and_prepare_revision(
    config_id,
    original_query,
    draft_output,
    validation_input,
    validation_agent
):
    """
    Handles:
    - calling validation agent
    - extracting validation feedback
    - preparing revision prompt for drafting agent

    Returns:
    {
        "config_id": str,
        "validation_feedback": str,
        "revision_input": str,
        "status": str
    }
    """

    print(f"Starting validation for config_id: {config_id}")

    # Step 1: Call validation agent
    response = validation_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": validation_input
            }
        ]
    })

    # Step 2: Safe response extraction
    try:
        validation_feedback = response["messages"][-1].content
    except:
        validation_feedback = str(response)

    print("\nVALIDATION FEEDBACK:\n")
    print(validation_feedback)

    # Step 3: Check if revision is needed
    if "no major issues" in validation_feedback.lower():
        return {
            "config_id": config_id,
            "validation_feedback": validation_feedback,
            "revision_input": None,
            "status": "approved"
        }

    # Step 4: Prepare drafting-ready revision prompt
    revision_input = f"""
        Please revise and improve the previous Clinical Study Report draft
        based on the validation feedback below.

        Original User Request:
        {original_query}

        Previous Draft:
        {draft_output}

        Validation Feedback:
        {validation_feedback}

        Instructions:
        - Fix all identified issues
        - Maintain ICH E3 compliance
        - Keep professional regulatory writing style
        - Do not remove valid existing sections
        - Improve completeness and accuracy

        Generate the improved draft now.
        """

    return {
        "config_id": config_id,
        "validation_feedback": validation_feedback,
        "revision_input": revision_input,
        "status": "needs_revision"
    }