# System Architecture

Matches the 6-layer architecture from the project plan (Section 10).

## Layer overview

| Layer | Components in this build | Purpose |
|---|---|---|
| User | React web app (`/web`), React Native Expo app (`/mobile`) | Employees/officers/admins interact via browser or Android app |
| Application | FastAPI backend (`/backend/app`) — routers, RBAC guards, ticket workflow | Business rules, auth, tickets, dashboard data |
| AI | Ollama (local LLM) + sentence-transformers embeddings | Generates grounded answers from retrieved document text |
| Knowledge | ChromaDB (persistent, one collection per department) + chunking/extraction in `rag_service.py` | Stores document vectors, finds relevant chunks |
| Data | PostgreSQL (Docker) / SQLite (local dev fallback) | Users, departments, tickets, chat logs, documents, audit logs |
| Deployment | `docker-compose.yml` (local demo) + notes for free-tier hosting | Offline demo primary; optional public showcase |

## Diagram

```mermaid
flowchart TB
    subgraph User["User Layer"]
        Web["React Web App"]
        Mobile["React Native (Expo) App"]
    end

    subgraph App["Application Layer (FastAPI)"]
        Auth["Auth / JWT / RBAC"]
        TicketSvc["Ticket Workflow"]
        DashSvc["Dashboard & Analytics"]
        AuditSvc["Audit Logging"]
    end

    subgraph AI["AI Layer"]
        Embed["sentence-transformers\n(embeddings)"]
        LLM["Ollama\n(local LLM)"]
    end

    subgraph Knowledge["Knowledge Layer"]
        Chroma["ChromaDB\n(per-department collections)"]
        Ingest["Document Ingestion\n(chunking, extraction)"]
    end

    subgraph Data["Data Layer"]
        PG["PostgreSQL\n(users, tickets, docs, logs)"]
    end

    subgraph Deploy["Deployment Layer"]
        Docker["Docker Compose\n(local demo)"]
        Cloud["Free-tier hosting\n(Render / HF Spaces / Cloudflare Pages)"]
    end

    Web --> Auth
    Mobile --> Auth
    Auth --> PG
    TicketSvc --> PG
    AuditSvc --> PG
    DashSvc --> PG

    Web -- "ask question" --> Embed
    Embed --> Chroma
    Chroma -- "top-k chunks" --> LLM
    LLM -- "grounded answer + sources" --> Web
    Ingest --> Chroma
    Ingest --> PG

    Docker -.-> PG
    Docker -.-> Chroma
    Docker -.-> LLM
    Cloud -.-> Web
```

## RAG request flow (detail)

```mermaid
sequenceDiagram
    participant E as Employee
    participant B as Backend (FastAPI)
    participant V as ChromaDB
    participant L as Ollama LLM

    E->>B: POST /api/chat/ask {department_id, question}
    B->>V: embed(question) + similarity search (top_k)
    V-->>B: matching chunks + scores
    B->>L: prompt with retrieved context
    alt Ollama reachable
        L-->>B: generated answer
    else Ollama unreachable/error
        B->>B: fall back to template answer using top chunk
    end
    B->>B: compute top_similarity, suggest_ticket flag
    B-->>E: answer + sources[] + suggest_ticket
    opt low similarity or user chooses to
        E->>B: POST /api/tickets (origin_chat_log_id set)
    end
```

## Key design decisions / assumptions

- **SQLite fallback**: local dev without Docker defaults to SQLite (explicitly allowed by the project plan); `docker-compose.yml` uses Postgres by default, per spec.
- **Embedding fallback**: if `sentence-transformers` can't download model weights (no internet), the system falls back to a lightweight hashing-based embedder rather than crashing. This is a deliberate robustness choice beyond the spec's explicit Ollama-only fallback requirement, since embedding-model download failures are just as likely to break a fresh-clone demo as an LLM outage.
- **One Chroma collection per department**: keeps documents/embeddings isolated per department without extra infrastructure, matching the "documents separated by department" security requirement.
- **Similarity → confidence score**: `score = 1 - (distance / 2)`, clamped to `[0, 1]`. This is an implementation choice (not specified in the plan) for turning Chroma's raw distance into an intuitive 0–1 number used for the ticket-suggestion threshold.
