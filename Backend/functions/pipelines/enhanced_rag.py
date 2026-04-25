# --- Enhanced RAG Pipeline Features ---
def rag_advanced(query, retriever, llm, top_k=5, min_score=0.2, return_context=False):
    """
    RAG Pipeline with extra features:
    - Returns answer, sources, confidence score, and optionally full context.
    """
    results = retriever.retrieve(query, top_k=top_k)
    if not results:
        return {'answer': "I do not have sufficient information in the provided documents to answer this accurately.", 'sources': [], 'confidence': 0.0, 'context': ''}

    # Prepare context and sources
    context = "\n\n---\n\n".join(
        f"[Source: {doc['metadata'].get('source_file','unknown')}]\n{doc['content']}"
        for doc in results
    )   


    sources = [{
        'source': doc['metadata'].get('source_file' ,'unknown'),
        'page': doc['metadata'].get('page', 'unknown'),
        'score': doc['similarity_score'],
        } 
        for doc in results
    ]
    confidence = sum(doc["similarity_score"] for doc in results) / len(results)

    # Generate answer
    prompt = f"""
            You are a Senior Regulatory Affairs and Life Sciences Intelligence Assistant specializing in FDA, EMA, and ICH-compliant regulatory documentation.

            You generate submission-ready regulatory drafts using ONLY the provided retrieved context.

            --------------------------------------------------
            STRICT RULES:

            1. Use ONLY provided context. Do NOT use external knowledge.
            2. Do NOT hallucinate missing information.
            3. If information is missing, explicitly state:
            "Information not available in retrieved context"
            4. Do NOT attempt to complete missing sections with assumptions.
            5. Maintain formal regulatory writing suitable for submission review.
            6. Clearly highlight compliance gaps and regulatory risks.
            7. Preserve structure only if supported by retrieved context.

            --------------------------------------------------
            Retrieved Context:
            {context}

            --------------------------------------------------
            Drafting Request:
            {query}

            --------------------------------------------------
            OUTPUT FORMAT:

            Title:
            Purpose:
            Key Regulatory Considerations:
            Draft Content:
            Missing Information Needed:
            Potential Regulatory Risks:

            --------------------------------------------------
            FINAL INSTRUCTION:
            Generate ONLY the regulatory draft. Do not include explanations or meta commentary.
            """
    response = llm.invoke(prompt)

    output= {
        'answer': response.content,
        'sources': sources,
        'confidence': confidence
    }

    if return_context:
        output['context'] = context
    return output

