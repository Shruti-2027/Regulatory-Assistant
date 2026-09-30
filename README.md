# 🧬 Regulatory Assistant

> **An AI-powered regulatory intelligence assistant for pharmaceutical and healthcare regulatory documentation using Retrieval-Augmented Generation (RAG), semantic search, and a Draft → Validate AI workflow.**

Regulatory Assistant is an AI-powered application designed to help users interact with complex pharmaceutical regulatory documentation through natural-language queries.

Instead of requiring users to manually search through hundreds or thousands of pages of regulatory documents, the system retrieves the most relevant regulatory information from a curated knowledge base and uses a Large Language Model (LLM) to generate a contextual response.

To improve reliability, the generated response passes through a **two-stage AI workflow** consisting of:

```text
User Query
    ↓
Document Retrieval
    ↓
Relevant Regulatory Context
    ↓
Drafting Agent
    ↓
Validation Agent
    ↓
Final Response
```

The application combines **FastAPI, React, LangChain, ChromaDB, Sentence Transformers, and Groq-hosted LLMs** into an end-to-end AI/RAG system.

---

# 📌 Table of Contents

* [Overview](#-overview)
* [Problem Statement](#-problem-statement)
* [Objectives](#-objectives)
* [Key Features](#-key-features)
* [System Architecture](#-system-architecture)
* [End-to-End Workflow](#-end-to-end-workflow)
* [RAG Pipeline](#-rag-pipeline)
* [Document Processing](#-document-processing)
* [Chunking Strategy](#-chunking-strategy)
* [Embedding Model](#-embedding-model)
* [Vector Database](#-vector-database)
* [Information Retrieval](#-information-retrieval)
* [AI Generation Pipeline](#-ai-generation-pipeline)
* [Drafting Agent](#-drafting-agent)
* [Validation Agent](#-validation-agent)
* [Technology Stack](#-technology-stack)
* [Project Structure](#-project-structure)
* [Backend Architecture](#-backend-architecture)
* [Frontend Architecture](#-frontend-architecture)
* [API Workflow](#-api-workflow)
* [Knowledge Base](#-knowledge-base)
* [Configuration](#-configuration)
* [Installation](#-installation)
* [Running the Application](#-running-the-application)
* [Example Query Flow](#-example-query-flow)
* [Why RAG](#-why-rag)
* [Why a Validation Stage](#-why-a-validation-stage)
* [Design Decisions](#-design-decisions)
* [Challenges](#-challenges)
* [Limitations](#-limitations)
* [Future Improvements](#-future-improvements)
* [My Contribution](#-my-contribution)
* [Team](#-team)
* [Disclaimer](#-disclaimer)

---

# 🌟 Overview

Regulatory documentation in the pharmaceutical and healthcare domain is often extensive, highly technical, and difficult to navigate.

Important information may be distributed across:

* ICH guidelines
* FDA guidance documents
* Technical regulatory documents
* Compliance-related documentation
* Pharmaceutical development guidelines

A conventional keyword-based search system may fail when the user's query and the wording in the source document are semantically related but use different terminology.

Regulatory Assistant addresses this problem through **semantic retrieval and Retrieval-Augmented Generation (RAG)**.

The application transforms regulatory documents into vector representations, stores them in a vector database, and retrieves relevant pieces of information whenever a user asks a question.

The retrieved information is then supplied to the language model as contextual evidence.

---

# 🎯 Problem Statement

Pharmaceutical regulatory professionals frequently need to locate precise information within large collections of regulatory documents.

Traditional workflows involve:

```text
Search document
      ↓
Read multiple sections
      ↓
Identify relevant information
      ↓
Interpret the context
      ↓
Prepare response
```

This process can become inefficient when:

* Documents are large.
* Information is distributed across multiple sections.
* Terminology differs between the user's query and the document.
* Multiple regulatory documents need to be consulted.
* Users need contextual rather than simple keyword-based answers.

The objective of Regulatory Assistant is to provide a conversational interface that can retrieve relevant regulatory information and generate an answer based on that retrieved evidence.

---

# 🎯 Objectives

The major objectives of the project are:

### 1. Simplify regulatory document search

Allow users to ask questions using natural language instead of manually searching through documents.

### 2. Implement semantic retrieval

Retrieve information based on meaning rather than exact keyword matching.

### 3. Ground LLM responses

Provide the LLM with relevant regulatory context before generating an answer.

### 4. Reduce unsupported generation

Use retrieved regulatory documents as the primary source of contextual information.

### 5. Validate generated responses

Introduce a separate validation stage that reviews the drafted response.

### 6. Build an end-to-end AI application

Integrate:

```text
Frontend
   +
Backend
   +
RAG
   +
Vector Database
   +
LLM
   +
Validation Workflow
```

into a single application.

---

# ✨ Key Features

## 📚 Regulatory Knowledge Base

The application uses regulatory documentation from sources including:

* ICH
* FDA

These documents form the knowledge base used during retrieval.

---

## 🔎 Semantic Search

Instead of depending entirely on keyword matching, documents are converted into vector embeddings.

This allows queries to retrieve semantically related content.

For example:

```text
Query:
"What are the requirements for stability testing?"
```

can retrieve a document section even if the exact phrase does not appear in that section.

---

## 🧠 Retrieval-Augmented Generation

The system uses RAG to combine:

```text
User Query
+
Retrieved Regulatory Context
+
LLM
```

The LLM generates its response using the retrieved context rather than relying only on its pretrained knowledge.

---

## ✍️ Drafting Agent

The Drafting Agent receives the user's query together with the retrieved regulatory context and generates an initial answer.

---

## ✅ Validation Agent

The generated answer is passed to a separate validation stage.

The validator evaluates the response against the available context and checks whether the generated answer is appropriately supported and relevant.

---

## 🔄 Two-Stage AI Workflow

The application follows:

```text
Retrieve
   ↓
Draft
   ↓
Validate
   ↓
Final Response
```

rather than:

```text
Query
   ↓
LLM
   ↓
Answer
```

---

# 📚 Knowledge Base

The knowledge base focuses on pharmaceutical and healthcare regulatory information.

Primary regulatory sources include:

### ICH

The International Council for Harmonisation provides guidelines covering areas relevant to pharmaceutical development and regulation.

### FDA

The U.S. Food and Drug Administration publishes regulatory guidance and documentation relevant to pharmaceutical and healthcare products.

These documents provide the contextual foundation for the RAG pipeline.

---

# 🎥 Demo

**Demo Video:**
https://youtu.be/nGKNmpRoDQ4

---

# 📂 Repository

**GitHub Repository:**
https://github.com/Shruti-2027/Regulatory-Assistant

---

# 👥 Project Collaboration

This project was developed collaboratively as a team project.

The responsibilities were divided across the team, with different contributors working on the application, AI/RAG pipeline, frontend, backend, and project documentation.


# 🏗️ System Architecture

```text
                         ┌───────────────────────┐
                         │       User            │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   React + Vite UI     │
                         └───────────┬───────────┘
                                     │
                                     │ API Request
                                     ▼
                         ┌───────────────────────┐
                         │       FastAPI         │
                         │       Backend         │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │     User Query        │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    Query Embedding    │
                         │ all-MiniLM-L6-v2      │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │       ChromaDB        │
                         │    Vector Retrieval   │
                         └───────────┬───────────┘
                                     │
                              Top-K Context
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    Drafting Agent     │
                         │     LangChain         │
                         │       + Groq          │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │  Generated Response   │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   Validation Agent    │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    Final Response     │
                         └───────────────────────┘
```

---

# 🔄 End-to-End Workflow

The application can be understood as six major stages.

## Stage 1 — Document Ingestion

Regulatory documents are collected and processed.

```text
Regulatory Documents
        ↓
Document Loader
        ↓
Text Extraction
```

---

## Stage 2 — Document Chunking

Large documents are divided into smaller pieces.

```text
Large Document
      ↓
Text Splitting
      ↓
Smaller Chunks
```

The project uses:

```text
Chunk Size    = 800
Chunk Overlap = 150
```

The overlap helps preserve context between neighboring chunks.

---

## Stage 3 — Embedding Generation

Every chunk is transformed into a numerical vector representation.

The project uses:

```text
all-MiniLM-L6-v2
```

with:

```text
Embedding Dimension = 384
```

Conceptually:

```text
Text Chunk
    ↓
Embedding Model
    ↓
384-dimensional vector
```

---

## Stage 4 — Vector Storage

The generated embeddings are stored in **ChromaDB**.

The database maintains the relationship between:

```text
Vector
   +
Original Document Content
   +
Metadata
```

This enables efficient similarity-based retrieval.

---

## Stage 5 — Retrieval

When the user submits a question, the query is converted into an embedding and compared against the vectors stored in ChromaDB.

```text
Query
 ↓
Query Embedding
 ↓
Similarity Search
 ↓
Relevant Chunks
```

The configured retrieval count is:

```text
Top K = 5
```

---

## Stage 6 — Generation and Validation

The retrieved context is passed to the AI workflow.

```text
Retrieved Context
       ↓
Drafting Agent
       ↓
Generated Response
       ↓
Validation Agent
       ↓
Final Response
```

---

# 🔍 RAG Pipeline

The Retrieval-Augmented Generation pipeline is the central component of the application.

```text
                 User Question
                       │
                       ▼
              Query Embedding
                       │
                       ▼
                Vector Search
                       │
                       ▼
               Top-K Documents
                       │
                       ▼
              Retrieved Context
                       │
                       ▼
              Prompt Construction
                       │
                       ▼
                     LLM
                       │
                       ▼
              Generated Response
```

The configured retrieval count is:

```text
Top K = 5
```

The system therefore retrieves the five most relevant chunks before generating the response.

---

# 📄 Document Processing

The quality of a RAG system depends heavily on how its source documents are processed.

The document processing pipeline is:

```text
PDF / Regulatory Document
          ↓
      Text Extraction
          ↓
      Text Cleaning
          ↓
       Chunking
          ↓
      Embeddings
          ↓
       ChromaDB
```

The indexed knowledge base was expanded during development as additional regulatory content was incorporated.

---

# ✂️ Chunking Strategy

Documents are divided into chunks rather than embedding entire documents as a single vector.

Configuration:

| Parameter       | Value |
| --------------- | ----: |
| Chunk Size      |   800 |
| Chunk Overlap   |   150 |
| Retrieval Count | Top 5 |

### Why chunk documents?

Consider a large regulatory document.

Creating a single embedding for the entire document would make retrieval too coarse.

Instead:

```text
Large document
       ↓
Multiple smaller chunks
       ↓
Individual embeddings
       ↓
Semantic retrieval
```

This allows the system to identify specific sections that are relevant to the user's query.

### Why overlap chunks?

Without overlap, important contextual information near a chunk boundary could be separated.

An overlap helps preserve information across those boundaries.

---

# 🧠 Embedding Model

The project uses:

```text
all-MiniLM-L6-v2
```

from the Sentence Transformers ecosystem.

The model generates:

```text
384-dimensional embeddings
```

These vectors represent the semantic meaning of text.

For example:

```text
"stability testing requirements"
```

and:

```text
"conditions and procedures used to evaluate pharmaceutical product stability"
```

may be semantically close even though they use different words.

This is one of the advantages of embedding-based retrieval over simple keyword matching.

---

# 🗄️ Vector Database — ChromaDB

**ChromaDB** is used as the vector database.

It stores:

```text
Document Chunk
      +
Embedding
      +
Metadata
```

When the user submits a query:

```text
Query
 ↓
Query Embedding
 ↓
Similarity Search
 ↓
Relevant Chunks
```

The retrieved chunks become the contextual input to the generation pipeline.

---

# 🔎 Information Retrieval

The system retrieves the most relevant chunks using vector similarity.

The retrieval pipeline can be represented as:

```text
User Query
     ↓
Query Embedding
     ↓
Compare against document vectors
     ↓
Rank by similarity
     ↓
Select Top 5
     ↓
Return relevant context
```

The retrieval step is important because the LLM does not need to process the entire regulatory knowledge base for every question.

Instead, only the most relevant information is passed to the generation stage.

---

# 🤖 AI Generation Pipeline

After retrieval, the system constructs a contextual prompt containing:

```text
User Question
+
Retrieved Regulatory Context
+
Generation Instructions
```

This information is provided to the LLM.

The project uses:

```text
Llama 3.1 8B Instant
```

through:

```text
Groq
ChatGroq
```

and integrates the model using **LangChain**.

---

# ✍️ Drafting Agent

The Drafting Agent is responsible for generating the initial answer.

Its workflow is:

```text
User Query
     +
Retrieved Context
     ↓
Drafting Agent
     ↓
Initial Response
```

The agent uses the retrieved regulatory information as its contextual foundation.

This separates:

```text
Information Retrieval
```

from:

```text
Response Generation
```

and makes the architecture easier to extend.

---

# ✅ Validation Agent

The generated response is not treated as the final answer immediately.

Instead:

```text
Drafted Response
       ↓
Validation Agent
       ↓
Validated Response
```

The validation stage checks whether the generated answer is consistent with the available regulatory context.

Important validation dimensions include:

### Accuracy

Does the response correctly represent the retrieved information?

### Relevance

Does the response address the user's question?

### Completeness

Does the response adequately cover the information needed?

### Regulatory Alignment

Does the response remain grounded in the provided regulatory context?

---

# 🔄 Draft → Validate Architecture

The core AI workflow is:

```text
┌──────────────┐
│ User Query   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Retrieve   │
│ Top 5 Chunks │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Drafting   │
│    Agent     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Drafted    │
│   Response   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Validation  │
│    Agent     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Final     │
│   Response   │
└──────────────┘
```

---

# 🛠️ Technology Stack

## Frontend

| Technology | Purpose                            |
| ---------- | ---------------------------------- |
| React      | User interface                     |
| Vite       | Frontend development/build tooling |

## Backend

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Python     | Backend language             |
| FastAPI    | REST API / backend framework |

## AI / LLM

| Technology           | Purpose                   |
| -------------------- | ------------------------- |
| LangChain            | LLM and RAG orchestration |
| Groq                 | LLM inference             |
| ChatGroq             | LangChain integration     |
| Llama 3.1 8B Instant | Response generation       |

## RAG

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| Sentence Transformers | Text embeddings              |
| all-MiniLM-L6-v2      | Embedding model              |
| ChromaDB              | Vector storage and retrieval |

## Knowledge Sources

* ICH regulatory guidelines
* FDA regulatory documentation

---

# 📊 RAG Configuration

| Component           | Configuration        |
| ------------------- | -------------------- |
| Embedding Model     | `all-MiniLM-L6-v2`   |
| Embedding Dimension | 384                  |
| Chunk Size          | 800                  |
| Chunk Overlap       | 150                  |
| Retrieved Chunks    | Top 5                |
| LLM                 | Llama 3.1 8B Instant |
| LLM Provider        | Groq                 |
| Vector Database     | ChromaDB             |
| RAG Framework       | LangChain            |

---

# 💡 Why RAG?

A general-purpose LLM has limitations when answering questions about specialized regulatory documentation.

Its internal knowledge may:

* Be incomplete
* Become outdated
* Lack access to project-specific documents
* Generate unsupported information

RAG addresses this by introducing an external knowledge source.

Instead of:

```text
Question → LLM → Answer
```

the system uses:

```text
Question
   ↓
Retrieve Evidence
   ↓
LLM + Evidence
   ↓
Answer
```

This makes the system better suited to domain-specific document question answering.

---

# 🛡️ Why Add a Validation Stage?

A single LLM generation step can produce an answer that appears convincing but does not accurately represent the source material.

The project therefore separates:

```text
Generation
```

from:

```text
Validation
```

This creates an additional verification layer.

The design follows:

```text
Retrieve evidence
       ↓
Generate response
       ↓
Validate response
```

rather than assuming that every generated answer is automatically correct.

---

# 🧩 Design Decisions

## Why FastAPI?

FastAPI provides a lightweight Python backend suitable for integrating:

* Machine learning models
* LLM APIs
* RAG pipelines
* Vector databases

It also makes it straightforward to expose the AI pipeline through APIs consumed by the React frontend.

---

## Why ChromaDB?

The application requires semantic vector retrieval rather than conventional relational querying.

ChromaDB provides a vector-store layer for:

```text
Embeddings
+
Documents
+
Similarity Search
```

---

## Why `all-MiniLM-L6-v2`?

The model provides compact semantic embeddings while keeping the vector representation relatively small.

Its 384-dimensional representation is suitable for semantic document retrieval without requiring extremely large embedding vectors.

---

## Why LangChain?

LangChain provides components for connecting:

```text
Document Retrieval
+
Embeddings
+
Vector Stores
+
LLMs
```

This makes it easier to structure the RAG pipeline and connect retrieval and generation stages.

---

## Why Groq?

Groq provides fast inference for supported language models.

This is useful for an interactive application where users expect relatively quick responses from the AI pipeline.

---

# 🏛️ Backend Architecture

The backend is responsible for:

1. Receiving user requests
2. Processing queries
3. Performing vector retrieval
4. Constructing contextual prompts
5. Calling the LLM
6. Running the validation workflow
7. Returning the final response

Conceptually:

```text
Frontend
   │
   │ HTTP Request
   ▼
FastAPI
   │
   ├── Query Processing
   │
   ├── Retrieval
   │      └── ChromaDB
   │
   ├── Drafting Agent
   │      └── Groq / Llama
   │
   └── Validation Agent
          └── Groq / Llama
   │
   ▼
Final Response
```

---

# 🌐 Frontend Architecture

The frontend is implemented using:

```text
React + Vite
```

Its primary responsibility is providing a user-friendly interface through which users can:

1. Enter regulatory questions
2. Submit queries
3. Communicate with the FastAPI backend
4. Receive and display generated responses

The frontend and backend are separated, allowing the AI pipeline to operate independently from the presentation layer.

---

# 🔌 API Workflow

The high-level communication flow is:

```text
React Frontend
      │
      │ HTTP Request
      ▼
FastAPI Backend
      │
      ▼
Query Processing
      │
      ▼
RAG Retrieval
      │
      ▼
AI Workflow
      │
      ▼
Validation
      │
      ▼
FastAPI Response
      │
      ▼
React Frontend
```

---

# 📁 Project Structure

The repository follows a frontend/backend architecture.

```text
Regulatory-Assistant/
│
├── backend/
│   ├── ...
│   └── ...
│
├── frontend/
│   ├── ...
│   └── ...
│
├── requirements.txt
├── README.md
└── ...
```

> Update this section with the exact repository structure if additional modules or directories are added.

---

# ⚙️ Configuration

The application requires the appropriate environment variables for external services.

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit API keys or other secrets to the repository.

If additional variables are required by the current implementation, add them to the environment configuration before running the application.

---

# 🚀 Installation

## Prerequisites

Make sure the following are installed:

* Python 3.x
* Node.js
* npm
* Git

---

## 1. Clone the Repository

```bash
git clone https://github.com/Shruti-2027/Regulatory-Assistant.git
```

Navigate into the project:

```bash
cd Regulatory-Assistant
```

---

## 2. Backend Setup

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Environment Variables

Create:

```text
.env
```

and configure the required API keys.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit `.env` files or API keys to GitHub.

---

## 4. Start Backend

Start the FastAPI application using the project's configured entry point.

For example:

```bash
uvicorn main:app --reload
```

The API should then be available through the configured local port.

> Replace `main:app` with the actual entry point used by the repository if different.

---

# 💻 Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The Vite development server will provide the frontend URL in the terminal.

---

# 🔬 Example Query Flow

Suppose the user asks:

```text
What are the regulatory considerations for stability testing?
```

The system processes the request as follows:

### Step 1 — Query

```text
"What are the regulatory considerations for stability testing?"
```

### Step 2 — Embedding

The query is converted into a 384-dimensional vector using:

```text
all-MiniLM-L6-v2
```

### Step 3 — Retrieval

ChromaDB searches the regulatory knowledge base and retrieves the top five relevant chunks.

```text
Query
 ↓
Vector Similarity
 ↓
Top 5 Chunks
```

### Step 4 — Context Construction

The retrieved chunks are supplied as contextual information to the Drafting Agent.

### Step 5 — Draft

The Llama model generates an initial response.

### Step 6 — Validation

The Validation Agent reviews the generated response against the retrieved regulatory context.

### Step 7 — Final Response

The validated response is returned to the frontend.

---

# 🧪 Application Flow

A complete user interaction can therefore be represented as:

```text
                    User
                     │
                     ▼
              ┌─────────────┐
              │ React / Vite│
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │   FastAPI   │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │   Retrieve  │
              │   Top 5     │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │   ChromaDB  │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │   Drafting  │
              │    Agent    │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ Validation  │
              │    Agent    │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │   Response  │
              └─────────────┘
```

---

# 🧠 Implementation Highlights

The project demonstrates practical implementation of several AI engineering concepts:

### Retrieval-Augmented Generation

The application combines external regulatory knowledge with LLM generation.

### Semantic Search

Document embeddings allow semantically related information to be retrieved.

### Vector Databases

ChromaDB provides persistent vector-based retrieval.

### LLM Integration

The project integrates Groq-hosted Llama models through LangChain.

### AI Workflow Design

The Drafting → Validation architecture separates response generation from response verification.

### Full-Stack AI Integration

The project connects:

```text
React
   ↕
FastAPI
   ↕
LangChain
   ↕
ChromaDB
   ↕
Groq / Llama
```

---

# ⚠️ Limitations

Although the system introduces retrieval and validation mechanisms, it should not be considered a replacement for professional regulatory expertise.

Potential limitations include:

* Retrieval quality depends on the quality of indexed documents.
* Incorrect or incomplete source documents can affect generated responses.
* Semantic retrieval may occasionally retrieve context that is related but not sufficiently specific.
* LLM-generated responses can still contain errors.
* Regulatory documents may change over time.
* The current system does not guarantee regulatory or legal correctness.

Therefore, important regulatory decisions should always be verified against the latest authoritative documentation.

---

# 🔮 Future Improvements

## 1. Source Citations

Return the exact regulatory document and section used to generate each part of the response.

```text
Answer
  ↓
Source Document
  ↓
Section / Page
```

---

## 2. Hybrid Retrieval

Combine:

```text
Semantic Search
+
Keyword Search
```

to improve retrieval for specialized regulatory terminology.

---

## 3. Reranking

Retrieve a larger candidate set and use a reranker to select the most relevant passages.

```text
Top 20 candidates
       ↓
Reranker
       ↓
Top 5 relevant chunks
```

---

## 4. Evaluation Framework

Introduce a dedicated evaluation dataset containing:

* Questions
* Expected answers
* Relevant source documents
* Ground-truth passages

This would allow systematic evaluation of:

* Retrieval accuracy
* Answer relevance
* Faithfulness
* Completeness

---

## 5. Continuous Knowledge Updates

Automate ingestion of new regulatory documents so that the knowledge base can remain synchronized with updated guidance.

---

## 6. Conversation Memory

Allow users to ask follow-up questions while maintaining relevant conversational context.

---

## 7. Authentication and Authorization

Add user authentication and role-based access for production environments.

---

## 8. Production Deployment

Deploy the complete system using scalable infrastructure:

```text
React Frontend
       +
FastAPI Backend
       +
Vector Database
       +
LLM Provider
```

---

# 🏆 Project Highlights

### AI / RAG

* Retrieval-Augmented Generation
* Semantic document search
* Vector embeddings
* ChromaDB
* LangChain
* LLM integration

### Agentic Workflow

* Drafting Agent
* Validation Agent
* Sequential AI workflow

### Backend

* FastAPI
* REST API
* AI service integration

### Frontend

* React
* Vite

### Domain

* Pharmaceutical regulatory documentation
* ICH
* FDA

---

# 🎥 Demo

A demonstration of the application is available here:

**Demo Video:**
https://youtu.be/nGKNmpRoDQ4

---

# 📂 Repository

**GitHub Repository:**

https://github.com/Shruti-2027/Regulatory-Assistant

---

# ⚠️ Disclaimer

Regulatory Assistant is an **educational and demonstration project**.

It is not intended to provide professional medical, legal, pharmaceutical, or regulatory advice.

The generated responses should not be used as the sole basis for regulatory submissions, compliance decisions, medical decisions, or other high-stakes decisions.

Users should always verify important information against the latest official regulatory sources and consult qualified professionals where appropriate.

---

# 📌 Summary

Regulatory Assistant demonstrates how a domain-specific AI assistant can be built by combining a **vector-based retrieval system with an LLM and an additional validation stage**.

The overall architecture is:

```text
                  ┌─────────────┐
                  │    User     │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ React/Vite  │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   FastAPI   │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   Query     │
                  │ Embedding   │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  ChromaDB   │
                  │  Retrieval  │
                  └──────┬──────┘
                         │
                     Top 5 Chunks
                         │
                         ▼
                  ┌─────────────┐
                  │   Drafting  │
                  │    Agent    │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Validation  │
                  │    Agent    │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │    Final    │
                  │   Answer    │
                  └─────────────┘
```

The project demonstrates an end-to-end implementation of a **domain-specific RAG application**, from regulatory document ingestion and vector retrieval to LLM-based generation and response validation.


