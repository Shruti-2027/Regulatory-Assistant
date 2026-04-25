import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from sentence_transformers import SentenceTransformer

### Read all the pdf's inside the directory

def process_all_pdfs(pdf_directory):
    """Process all PDF files in a directory"""
    all_documents = []
    pdf_dir = Path(pdf_directory)

    # Find all PDF files recursively
    pdf_files = list(pdf_dir.glob("**/*.pdf"))

    print(f"Found {len(pdf_files)} PDF files to process")

    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        try:
            loader = PyPDFLoader(str(pdf_file))
            documents = loader.load()

            # Add source information to metadata
            for doc in documents:
                doc.metadata['source_file'] = pdf_file.name
                doc.metadata['file_type'] = 'pdf'

            all_documents.extend(documents)
            print(f" Loaded {len(documents)} pages")
        
        except Exception as e:
            print(f" Error: {e} ")

    print(f"\nTotal documents loaded: {len(all_documents)}")
    return all_documents



### Text splitting get into chunks

def split_documents(documents, chunk_size=800, chunk_overlap=150):
    """Split documents into smaller chunks for better RAG performance"""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)

    # Remove very small / noisy chunks
    chunks = [
        chunk for chunk in chunks
        if len(chunk.page_content.strip()) > 100
    ]

    print(f"Split {len(documents)} documents into {len(chunks)} clean chunks")

    # Show example
    if chunks:
        print("\nExample chunk:")
        print(f"Content: {chunks[0].page_content[:300]}...")
        print(f"Metadata: {chunks[0].metadata}")

    return chunks