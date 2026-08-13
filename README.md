# Chatbot-Based Helpdesk for Government Employees and Departments

> Final Year Academic Project — a secure, department-wise support portal for government employees in India.

## Project Details

### Problem Statement

Design and develop a solution for a chatbot-based helpdesk for government employees and departments using modern technologies to improve performance, automation, security, scalability, and real-world usability.

### Proposed Solution

The solution has two connected parts: an AI chatbot for quick help and a ticketing system for issues that need an officer. The chatbot searches approved department documents for relevant information, uses a local open-source AI model to write a simple answer, and displays the source document name. If an answer is not reliable or an employee needs human support, the system creates a support ticket.

### Main Objective

To develop a secure AI-based helpdesk system that provides fast, department-wise support to government employees in India.

## Features

- Department-wise AI support for HR, Finance, IT, Pension, and Administration.
- Document-grounded answers with source references.
- Support ticket creation and tracking for human officer assistance.
- Role-based access for Employee, Officer, Department Admin, and Super Admin.
- Department document management, analytics, audit logs, and employee creation.

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Frontend | React, Vite, Tailwind CSS |
| Database | SQLite for local development; PostgreSQL with Docker |
| AI / RAG | SentenceTransformers, ChromaDB, Ollama |
| Authentication | JWT and bcrypt |
| Mobile | React Native / Expo |

## Team

| Role | Name | Roll Number |
|---|---|---|
| Team Leader | Syed Mohammed Tayab | 20231IST0040 |
| Team Member | Kuchi Sai Krishna | 20231IST0041 |
| Team Member | PVSM Yogesh Reddy | 20231IST0042 |

## Run Locally on Windows

Open this project folder in VS Code, then open two integrated terminals using **Terminal → New Terminal**. Keep the backend terminal running while using the website.

### Prerequisites

- Python 3.11 or later
- Node.js 18 or later
- npm

### PowerShell (including VS Code terminal)

**Terminal 1 — Backend**

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

If you activated the project-root virtual environment before entering `backend`, run:

```powershell
cd backend
uvicorn app.main:app --reload --port 8000
```

If PowerShell blocks activation, run this once in the same terminal and retry:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

**Terminal 2 — Frontend**

```powershell
cd web
npm install
npm run dev
```

Open the web application at `http://localhost:5173`.

### Command Prompt (cmd)

**Terminal 1 — Backend**

```cmd
cd backend
venv\Scripts\activate.bat
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend**

```cmd
cd web
npm install
npm run dev
```

### Useful Local URLs

| Service | URL |
|---|---|
| Web app | `http://localhost:5173` |
| Backend health check | `http://127.0.0.1:8000/health` |
| Backend API documentation | `http://127.0.0.1:8000/docs` |

## Demo Login Credentials

All current seeded demo accounts use the working password **`Demo@1234`**.

| Role | Email | Password | Department |
|---|---|---|---|
| Super Admin | `superadmin@demo.gov.in` | `Demo@1234` | All / System-wide |
| Dept Admin (HR) | `admin.hr@demo.gov.in` | `Demo@1234` | HR Department |
| Officer (HR) | `officer.hr@demo.gov.in` | `Demo@1234` | HR Department |
| Employee | `employee@demo.gov.in` | `Demo@1234` | HR Department |

> The earlier passwords `super123`, `admin123`, `officer123`, and `employee123` are not valid for the current seeded database.

## Questions You Can Ask the AI Assistant

### Finance Department

Ask about salary processing, tax deductions (TDS), travel allowances (TA/DA), and expense reimbursements.

- “When are monthly salary slips generated and where can I download them?”
- “How do I submit Form 12BB for Income Tax / TDS savings declaration?”
- “What is the procedure and daily rate for claiming Travel Allowance (TA/DA)?”
- “What documents are required to claim medical expense reimbursement?”

### Information Technology (IT Support)

Ask about email account setup, password resets, VPN access for remote work, and hardware/device allocation.

- “How do I reset my government NIC email account password?”
- “What are the steps to set up VPN access for secure remote work?”
- “How do I request a new laptop or official workstation device?”
- “What is the policy for report submission and raising IT support tickets?”

### Pension & Retirement

Ask about qualifying service years, gratuity calculations, pension schemes (NPS/OPS), and family pension rules.

- “How is the Service Gratuity and Commutation of Pension calculated?”
- “What is the eligibility requirement for Family Pension?”
- “How do I submit my annual Life Certificate (Jeevan Pramaan) online?”
- “What documents are needed for voluntary retirement (VRS) processing?”

### Administration & Facilities

Ask about office timings, visitor pass applications, vehicle parking permits, and official stationery requests.

- “What are the standard working hours and lunch break timings?”
- “How can I request a visitor pass for an external guest or vendor?”
- “What is the procedure to get an official vehicle parking sticker?”
- “How do I place a request for office stationery or computer accessories?”

## Repository Structure

```text
backend/        FastAPI application, APIs, models, services, and tests
web/            React web application
mobile/         React Native / Expo mobile application
demo-data/      Department policy and helpdesk documents
docs/           Architecture, API, testing, and user documentation
```

## Testing

```powershell
# From the project root
python smoke_test.py

# Backend tests
cd backend
pytest -v
```
