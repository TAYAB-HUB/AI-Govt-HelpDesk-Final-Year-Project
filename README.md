# 🏛️ AI-Powered Multi-Department Helpdesk & Smart Support System

> **Final Year Academic Project Prototype**  
> An enterprise-grade, offline-capable AI Helpdesk & RAG-driven Support System designed specifically for government employees in India.

---

## 📌 Executive Summary

Government departments handle thousands of administrative, policy, and procedural inquiries daily—spanning **HR, Finance, IT, Pension, and General Administration**. Traditional manual support channels suffer from response delays, inconsistent policy interpretation, and heavy officer workload.

This system solves these issues through a **hybrid AI + Human Officer architecture**:
1. **🤖 Instant RAG Chatbot**: Answers employee questions using local vector search (ChromaDB) and Ollama LLM, providing **exact source citations** from official department PDF/text policy documents.
2. **🎫 Intelligent Ticket System**: Automatically or manually escalates unresolved queries to human officers in the specific target department, complete with status tracking, comment history, and audit logs.
3. **🔐 Multi-Tier Role-Based Control (RBAC)**: Enforces strict operational boundaries across **4 distinct user roles**: *Employee*, *Department Officer*, *Department Admin*, and *Super Admin*.
4. **💰 Zero Cloud / Zero API Cost**: 100% open-source stack designed to run fully offline using local LLMs (Ollama + LLaMA 3.2) and local vector embeddings.

---

## 🌟 Key Features

### 🔍 1. Document-Grounded RAG (Retrieval-Augmented Generation)
- **Local Embeddings**: Converts uploaded official government policy documents into vector embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
- **Vector Search**: Performs fast cosine similarity retrieval in **ChromaDB**.
- **LLM Synthesis**: Generates accurate natural-language answers using **Ollama (LLaMA 3.2)**.
- **Source Citation**: Every response includes clickable source citations (document name, section, and confidence score) to guarantee accuracy and transparency.
- **Fallback Mode**: Includes an offline template-based fallback generator if Ollama is unreachable.

### 🎫 2. Lifecycle Support Ticketing
- **One-Click Escalation**: Convert any chat session directly into an official support ticket.
- **Smart Routing**: Auto-routes tickets to officers in the relevant department (HR, Finance, IT, Pension, Admin).
- **Status Workflow**: Tracks tickets through `OPEN` ➔ `IN_PROGRESS` ➔ `RESOLVED` / `CLOSED`.
- **Internal & Public Comments**: Multi-party conversation threads between employees and assigned officers.

### 👥 3. Multi-Role Web & Mobile Portals
- **Employee Portal**: Ask policy questions via Chat, raise tickets, and track resolution status.
- **Officer Workspace**: Filter assigned department tickets, update status, respond to queries, and add notes.
- **Department Admin Dashboard**: Manage department documents (upload/delete), reindex vector store, view team analytics, and manage department staff.
- **Super Admin Suite**: System-wide oversight, cross-department analytics, audit log inspection, and global user management.
- **📱 Mobile App**: Native mobile app (React Native / Expo) tailored for employees to query policies and view tickets on the go.

### 📊 4. Real-Time Analytics & Audit Trails
- **Interactive Dashboards**: Built with Recharts showing ticket volume by department, average resolution times, and RAG query frequency.
- **Security Audit Logs**: Logs all document uploads, role modifications, login attempts, and ticket actions.

---

## 🛠️ Technology Stack

| Layer | Component | Technology Used |
|---|---|---|
| **Backend** | REST API | FastAPI (Python 3.11+) |
| | Database ORM | SQLAlchemy 2.0 + Alembic Migrations |
| | Data Validation | Pydantic v2 |
| | Authentication | OAuth2 + JWT (python-jose) + Bcrypt |
| **AI / RAG** | Vector Database | ChromaDB |
| | Embeddings Model | SentenceTransformers (`all-MiniLM-L6-v2`) |
| | LLM Engine | Ollama (`llama3.2`) |
| | Document Processing | PyPDF + Recursive Text Splitters |
| **Web Frontend**| Framework & Build | React 18 + Vite |
| | Styling & UI | Tailwind CSS + Lucide React Icons |
| | State & Routing | React Context API + React Router v6 |
| | Data Visualization | Recharts |
| **Mobile App** | Cross-Platform | React Native + Expo |
| **Database** | Primary DB | PostgreSQL 15 (Docker) / SQLite (Dev Fallback) |
| **DevOps** | Containerization | Docker & Docker Compose |

---

## 📁 Repository Structure

```
ai-govt-helpdesk/
├── backend/                  # FastAPI Application & RAG Engine
│   ├── alembic/              # Database migration scripts
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Configuration, Database, Security & Dependencies
│   │   ├── models/           # SQLAlchemy Data Models (User, Ticket, Document, Audit, Dept)
│   │   ├── routers/          # Route handlers (Auth, Chat, Tickets, Documents, Analytics)
│   │   ├── schemas/          # Pydantic Request/Response validation schemas
│   │   ├── services/         # Business logic (RAG Service, Ticket Service, Audit Service)
│   │   ├── seed/             # Seed data scripts
│   │   └── main.py           # FastAPI entrypoint
│   ├── tests/                # Pytest unit and integration test suite
│   ├── Dockerfile
│   └── requirements.txt
├── web/                      # React 18 Web Dashboard
│   ├── src/
│   │   ├── api/              # Axios HTTP client configuration
│   │   ├── components/       # Reusable UI components & Layouts
│   │   ├── context/          # Auth & Global State Context
│   │   ├── pages/            # Role-Based Dashboards & Pages (Employee, Officer, Admin)
│   │   ├── App.jsx           # App Routing
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── vite.config.js
│   └── package.json
├── mobile/                   # React Native (Expo) Employee App
│   ├── src/
│   │   ├── context/          # Mobile Auth Context
│   │   ├── screens/          # Mobile Screen Views (Login, Chat, Tickets, CreateTicket)
│   │   └── services/         # API Service Calls
│   ├── App.js
│   ├── app.json
│   └── package.json
├── docs/                     # Comprehensive System Documentation
│   ├── architecture.md       # Architecture specification & flow diagrams
│   ├── report-skeleton.md    # Final Year Project Report Skeleton
│   └── test-case-list.md     # QA Test Cases & Validation Matrix
├── demo-data/                # Pre-packaged Sample Government Policy Documents
│   ├── hr/                   # HR Leave & Attendance Policies
│   ├── finance/              # Expense Reimbursements & Tax Declarations
│   ├── it/                   # Password Reset & VPN Access Manuals
│   ├── pension/              # GPF Withdrawal & Pension Rules
│   └── admin/                # Visitor & Vehicle Parking Guidelines
├── docker-compose.yml        # Docker Multi-Container Orchestration
├── seed.py                   # Automated Database Seeding Script
├── smoke_test.py             # E2E Smoke Testing Suite
└── README.md
```

---

## ⚡ Quick Start Guide

### Prerequisites
- [Git](https://git-scm.com/)
- [Docker & Docker Desktop](https://www.docker.com/) (Recommended) **OR** [Python 3.11+](https://www.python.org/) & [Node.js 18+](https://nodejs.org/)
- [Ollama](https://ollama.com/) (for local LLM execution)

---

### Option A: Run via Docker Compose (Recommended)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/TAYAB-HUB/AI-Govt-HelpDesk-Final-Year-Project.git
   cd AI-Govt-HelpDesk-Final-Year-Project
   ```

2. **Ensure Ollama is Running & Pull the LLaMA Model**:
   ```bash
   # In your terminal host machine:
   ollama pull llama3.2
   ollama serve
   ```

3. **Start All Containers**:
   ```bash
   docker-compose up --build
   ```
   *This starts PostgreSQL, FastAPI Backend, and React Web App.*

4. **Seed Database & Ingest Demo Policy Documents**:
   Open a new terminal window and run:
   ```bash
   docker-compose exec backend python seed.py
   ```

5. **Access the Applications**:
   - 🌐 **Web Dashboard**: [http://localhost:5173](http://localhost:5173) (or `http://localhost:8080`)
   - 📖 **Interactive API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - 📑 **ReDoc API Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Option B: Local Setup Without Docker (Fast Development)

#### 1. Backend Setup (FastAPI + SQLite/Postgres)
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run database migrations
alembic upgrade head

# Seed initial departments, users, and documents into ChromaDB
python seed.py

# Launch FastAPI server
uvicorn app.main:app --reload --port 8000
```

#### 2. Web Frontend Setup (React 18 + Vite)
```bash
# Open a new terminal in the root directory:
cd web

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
*Web App will be live at `http://localhost:5173`.*

#### 3. Mobile App Setup (React Native + Expo)
```bash
# Open a new terminal in the root directory:
cd mobile

# Install dependencies
npm install

# Start Expo dev server
npx expo start
```
*Scan the generated QR code with the **Expo Go** app on your iOS/Android phone or launch an emulator.*

---

### Option C: Run in Visual Studio Code (VS Code Tasks)

1. **Open the Project Folder in VS Code**:
   `File` -> `Open Folder...` -> Select `AI-Govt-HelpDesk-Final-Year-Project`.

2. **Method 1 — Run via Pre-configured VS Code Tasks (Easiest)**:
   - Press `Ctrl + Shift + B` (or `Cmd + Shift + B` on Mac).
   - Select **`🚀 Start Full Helpdesk System (Backend + Web)`**.
   - VS Code will automatically spin up both the FastAPI Backend (`http://localhost:8000`) and the React Web App (`http://localhost:5173`) in dedicated split terminals!

3. **Method 2 — Run via Integrated Terminals**:
   - Open VS Code Terminal (`Ctrl + ~`).
   - Split or create 2 terminals (`Ctrl + Shift + 5` or click `+`):
     - **Terminal 1 (Backend)**:
       ```powershell
       cd backend
       .\venv\Scripts\activate
       uvicorn app.main:app --reload --port 8000
       ```
     - **Terminal 2 (Web App)**:
       ```powershell
       cd web
       npm run dev
       ```

---

## 🔑 Default Demo Login Credentials

All seeded accounts are initialized with password: **`Demo@1234`**

| Role | User Email | Assigned Dept | Access Scope & Permissions |
|---|---|---|---|
| 👤 **Employee** | `employee@demo.gov.in` | HR | Ask AI queries, create/track tickets, view own history |
| 🛡️ **Officer (HR)** | `officer@demo.gov.in` | HR | View/manage HR tickets, add internal notes, change status |
| 🛡️ **Officer (Finance)**| `finance.officer@demo.gov.in` | Finance | View/manage Finance tickets & respond to inquiries |
| 🛡️ **Officer (IT)** | `it.officer@demo.gov.in` | IT | View/manage IT department tickets |
| 🛡️ **Officer (Pension)**| `pension.officer@demo.gov.in` | Pension | View/manage Pension department tickets |
| 🛡️ **Officer (Admin)**  | `admin.officer@demo.gov.in` | Administration| View/manage Admin department tickets |
| 🏢 **Dept Admin** | `deptadmin@demo.gov.in` | HR | Upload policy PDFs/docs, reindex ChromaDB, department staff |
| 👑 **Super Admin** | `superadmin@demo.gov.in` | System-wide | Full system access, audit logs, cross-dept analytics |

---

## 🧪 Testing & Verification

### 1. Run Automated E2E Smoke Tests
A comprehensive smoke test script validates health checks, auth login, RAG query flow, and ticket creation:
```bash
python smoke_test.py
```

### 2. Run Backend Unit Tests (Pytest)
```bash
cd backend
pytest -v
```

---

## 📜 Documentation Index

For detailed technical design documents, refer to the [`/docs`](./docs) folder:
- 📐 [`docs/architecture.md`](./docs/architecture.md): Complete multi-tier system architecture diagrams & RAG flow.
- 📋 [`docs/test-case-list.md`](./docs/test-case-list.md): Detailed software test cases and functional coverage matrix.
- 📄 [`docs/report-skeleton.md`](./docs/report-skeleton.md): Academic thesis/project report structure.

---

## 🤝 Academic & Open Source License

This project was developed as a **Final Year Computer Science Engineering Project**.  
It is built strictly for academic presentation, evaluation, and educational demonstration purposes (**not affiliated with or officially deployed by any government entity**).

Released under the **MIT License**.
