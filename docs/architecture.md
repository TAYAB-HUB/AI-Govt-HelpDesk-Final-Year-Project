# System Architecture

## Overview

The AI Government Helpdesk system follows a **6-layer architecture** designed for modularity, scalability, and offline capability.

## Architecture Diagram (Mermaid)

```mermaid
graph TB
    subgraph "User Layer"
        WebApp[React Web App]
        MobileApp[React Native Mobile App]
    end
    
    subgraph "Application Layer"
        API[FastAPI Backend]
        Auth[JWT Authentication]
        RBAC[Role-Based Access Control]
        Tickets[Ticket Management]
    end
    
    subgraph "AI Layer"
        Ollama[Ollama LLM Runtime]
        Embeddings[Sentence Transformers]
        RAG[RAG Pipeline]
    end
    
    subgraph "Knowledge Layer"
        Chroma[ChromaDB Vector Store]
        DocProcessor[Document Processor]
    end
    
    subgraph "Data Layer"
        Postgres[(PostgreSQL)]
        FileStore[File Storage]
    end
    
    subgraph "Deployment Layer"
        Docker[Docker Compose]
        LocalDemo[Local Ollama Instance]
    end
    
    WebApp --> API
    MobileApp --> API
    API --> Auth
    API --> RBAC
    API --> Tickets
    API --> RAG
    RAG --> Ollama
    RAG --> Embeddings
    RAG --> Chroma
    DocProcessor --> Chroma
    API --> Postgres
    API --> FileStore
    Docker --> API
    Docker --> Postgres
    Docker --> Chroma
    LocalDemo --> Ollama