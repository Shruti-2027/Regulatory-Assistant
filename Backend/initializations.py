from functions.Initializations.data_loading import process_all_pdfs
from functions.Initializations.data_loading import split_documents
from functions.Initializations.embedding_manager import EmbeddingManager
from functions.Initializations.vectore_store import VectorStore
from functions.pipelines.retriever_pipeline import RAGRetriever


def build_rag_system():
    # Process all PDFs in the data directory
    all_pdf_documents = process_all_pdfs("./data/Guidelines")

    # Chunking
    chunks = split_documents(all_pdf_documents)

    # Embeddings
    embedding_manager = EmbeddingManager()
    texts = [doc.page_content for doc in chunks]
    embeddings = embedding_manager.generate_embeddings(texts)

    # Vector store
    vectorstore = VectorStore()
    vectorstore.add_documents(chunks, embeddings)

    # Retriever
    rag_retriever = RAGRetriever(vectorstore, embedding_manager)

    return rag_retriever