# Database ER Diagram

```mermaid
erDiagram
    DEPARTMENT ||--o{ USER : "employs"
    DEPARTMENT ||--o{ DOCUMENT : "owns"
    DEPARTMENT ||--o{ TICKET : "routes to"
    DEPARTMENT ||--o{ CHAT_LOG : "scoped to"

    USER ||--o{ TICKET : "creates"
    USER ||--o{ TICKET : "assigned (nullable)"
    USER ||--o{ TICKET_COMMENT : "authors"
    USER ||--o{ CHAT_LOG : "asks"
    USER ||--o{ FEEDBACK : "gives"
    USER ||--o{ AUDIT_LOG : "performs (nullable)"

    TICKET ||--o{ TICKET_COMMENT : "has"
    CHAT_LOG ||--o{ FEEDBACK : "receives"
    CHAT_LOG ||--o| TICKET : "may originate"

    DEPARTMENT {
        int id PK
        string name
        string code
        string description
        datetime created_at
    }

    USER {
        int id PK
        string full_name
        string email
        string hashed_password
        enum role "employee|officer|dept_admin|super_admin"
        int department_id FK
        bool is_active
        datetime created_at
    }

    DOCUMENT {
        int id PK
        int department_id FK
        string title
        string filename
        string source_type "upload|seed"
        int raw_text_char_count
        int chunk_count
        int uploaded_by_id FK
        datetime created_at
    }

    CHAT_LOG {
        int id PK
        int user_id FK
        int department_id FK
        text question
        text answer
        text sources_json
        float top_similarity
        bool suggested_ticket
        string llm_provider_used
        datetime created_at
    }

    FEEDBACK {
        int id PK
        int chat_log_id FK
        int user_id FK
        enum vote "up|down"
        datetime created_at
    }

    TICKET {
        int id PK
        int department_id FK
        int created_by_id FK
        int assigned_to_id FK
        string category
        string subject
        text description
        enum priority "low|medium|high|urgent"
        enum status "open|in_progress|resolved|closed"
        int origin_chat_log_id FK
        datetime created_at
        datetime updated_at
    }

    TICKET_COMMENT {
        int id PK
        int ticket_id FK
        int author_id FK
        text body
        enum status_change_to "nullable"
        datetime created_at
    }

    AUDIT_LOG {
        int id PK
        int actor_id FK
        string action
        string target_type
        int target_id
        text detail
        datetime created_at
    }
```

Note: document *content* (chunked text + embeddings) lives in ChromaDB, not
Postgres/SQLite — the `DOCUMENT` table above only stores metadata
(title, filename, chunk count). This keeps the relational schema clean and
matches the plan's "Knowledge layer" being a separate store from the
"Data layer" (Section 10).
