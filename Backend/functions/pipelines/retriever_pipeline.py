from typing import List, Any, Tuple, Dict, Optional
from functions.Initializations.embedding_manager import EmbeddingManager
from functions.Initializations.vectore_store import VectorStore


class RAGRetriever:
    """
    Handles query-based retrieval from shared vector store
    for Drafting + Validation Agents
    """

    def __init__(self, vector_store: VectorStore, embedding_manager: EmbeddingManager):
        """
        Initialize the retriever
        
        Args:
            vector_store: Vector store containing document embeddings
            embedding_manager: Manager for generating query embeddings
        """
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    def retrieve(self, query: str, top_k: int=5, score_threshold: float = 0.0 , metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
            Retrieve relevant documents using semantic search + metadata filtering

            Args:
                query: User query
                top_k: Number of top documents
                score_threshold: Minimum similarity threshold
                metadata_filter: Optional ChromaDB where filter

            Returns:
                List of retrieved documents
        """
        print(f"Retrieving documents for query: '{query}'")
        print(f"Top K: {top_k}, Score threshold: {score_threshold}")
        print(f"Metadata Filter: {metadata_filter}")

        # Generate query embedding
        query_embedding = self.embedding_manager.generate_single_embedding(query)
        query_embedding = query_embedding.astype(float) 

        # Search in vector store
        try:
            # Query vector store
            query_params = {
                "query_embeddings": [query_embedding.tolist()],
                "n_results": top_k,
                "include": ["documents", "metadatas", "distances"]
            }

            # Apply metadata filtering if available
            if metadata_filter:
                query_params["where"] = metadata_filter

            results = self.vector_store.collection.query(**query_params)

            # Process results
            
            retrieved_docs = []

            documents = results.get("documents", [])
            metadatas = results.get("metadatas", [])
            distances = results.get("distances", [])
            ids = results.get("ids", [])

            if not documents or len(documents) == 0 or len(documents[0]) == 0:
                print("No documents found")
                return []

            documents = documents[0]
            metadatas = metadatas[0] if metadatas else [{}] * len(documents)
            distances = distances[0] if distances else [1.0] * len(documents)
            ids = ids[0] if ids else [f"unknown_{i}" for i in range(len(documents))]

            for i, (doc_id, document, metadata, distance) in enumerate(
                    zip(ids, documents, metadatas, distances)):

                similarity_score = 1 - distance

                retrieved_docs.append({
                    "id": doc_id,
                    "content": document,
                    "metadata": metadata,
                    "similarity_score": similarity_score,
                    "rank": i + 1
                })

            print(f"Retrieved {len(retrieved_docs)} documents")
            return retrieved_docs

        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []
                
