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



