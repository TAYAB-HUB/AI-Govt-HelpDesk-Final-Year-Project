# AI-Based Multi-Department Helpdesk Chatbot for Government Employees in India

An academic final-year project prototype (**not a real government system**).
Employees ask questions, get document-grounded (RAG) answers with source
citations, and can raise/track support tickets when the chatbot can't help.
Departments: HR, Finance, IT, Pension, Administration.

Built to the project plan's hard constraints: no paid AI APIs, no paid cloud
services, runnable fully offline via Docker Compose + Ollama.

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI, SQLAlchemy 2.x, Alembic, Pydantic v2, JWT (python-jose), passlib/bcrypt |
| AI | Ollama (local LLM), sentence-transformers, ChromaDB, pypdf |
| Database | PostgreSQL (Docker) / SQLite (local dev fallback) |
| Web | React 18, Vite, Tailwind CSS v4, React Router |
| Mobile | React Native + Expo (Employee role) |
| Infra | Docker + docker-compose |

## Repository layout

```
ai-govt-helpdesk/
  backend/           FastAPI app, RAG pipeline, Alembic, tests, seed script
  web/                React + Vite web app
  mobile/             Expo app (employee role)
  docs/               Architecture, ER diagram, API reference, user manual,
                       test case list, report skeleton
  demo-data/          15 sample department documents used for seeding
  docker-compose.yml
```

## Option A — Run everything with Docker (recommended for the faculty demo)

**Prerequisites:** Docker + Docker Compose installed.

```bash
docker compose up --build
```

This starts Postgres, the FastAPI backend (auto-runs Alembic migrations +
seed script on boot), Ollama, and the web frontend.

**One manual step required — pull an LLM model into Ollama** (only needed
once; models are cached in the `ollama_data` volume):

```bash
docker compose exec ollama ollama pull llama3.2
```

Until you do this, the chatbot still works via the built-in template
fallback (no crash) — it just won't use a real LLM for generation.

Then open:
- Web app: http://localhost:8080
- API docs (Swagger): http://localhost:8000/docs

## Option B — Run locally without Docker (fastest for development)

### Backend

```bash
cd backend
python3 -m venv venv && source venv/bin/activate   # or your preferred venv tool
pip install -r requirements.txt
cp .env.example .env          # SQLite by default — no Postgres needed
alembic upgrade head
python -m app.seed.seed       # creates departments, demo users, ingests demo-data/
uvicorn app.main:app --reload --port 8000
```

Backend is now at http://localhost:8000 (Swagger UI at `/docs`).

**Ollama (optional but recommended):** install from https://ollama.com,
then `ollama pull llama3.2` and run `ollama serve`. If you skip this,
set `LLM_PROVIDER=template` in `.env` (or just leave it — the system
auto-falls-back if Ollama isn't reachable).

### Web frontend

```bash
cd web
npm install
cp .env.example .env    # points at http://localhost:8000 by default
npm run dev
```

Open http://localhost:5173.

### Mobile app (Expo)

```bash
cd mobile
npm install
cp .env.example .env    # set EXPO_PUBLIC_API_BASE_URL to your machine's LAN IP,
                         # not localhost, if testing on a physical phone
npx expo start
```

Scan the QR code with the Expo Go app, or run on an emulator.

## Default demo logins

All seeded accounts use the password: **`Demo@1234`**

| Role | Email | Department |
|---|---|---|
| Employee | employee@demo.gov.in | HR |
| Officer | officer@demo.gov.in | HR |
| Department Admin | deptadmin@demo.gov.in | HR |
| Super Admin | superadmin@demo.gov.in | (all) |
| Officer | finance.officer@demo.gov.in | Finance |
| Officer | it.officer@demo.gov.in | IT |
| Officer | pension.officer@demo.gov.in | Pension |
| Officer | admin.officer@demo.gov.in | Administration |

These are obviously-fake demo credentials for local/offline evaluation only.

## Running tests

```bash
# Backend (pytest) — auth, RBAC, tickets, RAG retrieval
cd backend && pytest -v

# Frontend (Vitest + React Testing Library)
cd web && npm test
```

## Documentation

See `/docs`:
- `architecture.md` — 6-layer architecture + Mermaid diagrams
- `database-er-diagram.md` — ER diagram
- `api-reference.md` — endpoint summary (full OpenAPI at `/docs` on the running backend)
- `user-manual.md` — per-role walkthrough
- `test-case-list.md` — automated + manual test cases
- `report-skeleton.md` — final report headings, ready to fill in

## Known limitations

- **Embedding model download requires internet on first run.** `sentence-transformers`
  needs to download `all-MiniLM-L6-v2` from Hugging Face once. If that's
  unavailable, the system automatically falls back to a much weaker
  hashing-based embedder instead of crashing — retrieval quality will be
  noticeably worse in that mode. For your demo, run it once with internet
  access so the model is cached locally afterward.
- **Ollama must be running for real LLM-generated answers.** Without it,
  answers are template-based (a direct excerpt of the best-matching
  document chunk) rather than a natural-language synthesis — still
  functional and still source-cited, just less fluent.
- **Frontend automated tests are shallow** — only shared UI components have
  Vitest coverage; page-level/integration tests for Chat, Tickets, and the
  dashboards are not yet written.
- **This is an academic prototype.** It uses fictional demo documents and
  demo accounts only — do not connect it to real employee data or deploy
  it as an actual government system.
- **Free hosting tiers may sleep or rate-limit.** The Docker/Ollama local
  demo is the primary, reliable presentation method per the project plan's
  own risk assessment (Section 17).

## License / academic use

Built as a final-year academic project prototype. Not affiliated with or
endorsed by any government body.
