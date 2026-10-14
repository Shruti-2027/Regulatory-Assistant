def validate_and_prepare_revision(
    config_id,
    original_query,
    draft_output,
    validation_input,
    validation_agent,
    retriever
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

    # Step 1: Retrieve regulatory context
    results = retriever.retrieve(original_query, top_k=5)

    context = "\n\n---\n\n".join(
        f"[Source: {doc.get('metadata', {}).get('source_file', 'unknown')}]\n"
        f"{doc.get('content', '')}"
        for doc in results
    )

    if not context:
        context = "No relevant regulatory context was retrieved."

    # Step 2: Call validation agent with actual inputs
    user_message = f"""
    REGULATORY CONTEXT:
    {context}

    ORIGINAL USER REQUEST:
    {original_query}

    DOCUMENT TO VALIDATE:
    {draft_output}

    VALIDATION REQUIREMENTS:
    {validation_input}

    Return the validation result in the format specified
    by your system instructions.
    """

    response = validation_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ]
    })


    # Step 3: Extract validation response safely
    validation_feedback = ""

    try:
        messages = response.get("messages", [])

        if messages:
            validation_feedback = messages[-1].content or ""

    except (AttributeError, KeyError, IndexError, TypeError) as e:
        print(f"Validation response extraction error: {e}")
        print(f"Response type: {type(response)}")
        print(f"Raw response: {response}")

    if not validation_feedback.strip():
        print("WARNING: Validation agent returned empty feedback.")
        print(f"Raw validation response: {response}")
        raise ValueError("Validation agent returned empty feedback.")

    print("\nVALIDATION FEEDBACK:\n")
    print(validation_feedback)
    # Step 4: Check if revision is needed
    if "DOCUMENT IS SUBMISSION READY" in validation_feedback.upper():
        return {
            "config_id": config_id,
            "validation_feedback": validation_feedback,
            "revision_input": None,
            "status": "approved"
        }

    # Step 5: Prepare drafting-ready revision prompt
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