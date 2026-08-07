# Test Case List

## Automated (pytest — `backend/tests/`)

| ID | Test | File | What it verifies |
|---|---|---|---|
| T01 | `test_login_success` | test_auth_rbac.py | Valid credentials return a JWT |
| T02 | `test_login_wrong_password_fails` | test_auth_rbac.py | Wrong password → 401 |
| T03 | `test_register_and_login_new_user` | test_auth_rbac.py | New user can register then log in |
| T04 | `test_register_duplicate_email_fails` | test_auth_rbac.py | Duplicate email → 400 |
| T05 | `test_me_endpoint_requires_token` | test_auth_rbac.py | `/me` without token → 401 |
| T06 | `test_me_endpoint_with_token` | test_auth_rbac.py | `/me` returns the correct profile |
| T07 | `test_employee_cannot_create_department` | test_auth_rbac.py | RBAC: employee blocked from admin action → 403 |
| T08 | `test_super_admin_can_create_department` | test_auth_rbac.py | RBAC: super_admin allowed → 201 |
| T09 | `test_chunk_text_splits_long_text` | test_rag.py | Chunking respects size/overlap |
| T10 | `test_chunk_text_empty_returns_empty_list` | test_rag.py | Empty input handled safely |
| T11 | `test_ingest_and_retrieve_roundtrip` | test_rag.py | Document ingested is retrievable by a relevant query |
| T12 | `test_retrieve_on_empty_collection_returns_no_hits` | test_rag.py | No crash on empty department knowledge base |
| T13 | `test_generate_answer_template_mode_with_no_hits` | test_rag.py | Fallback answer suggests a ticket when nothing matches |
| T14 | `test_generate_answer_template_mode_with_hits` | test_rag.py | Fallback answer cites the source document |
| T15 | `test_employee_can_create_ticket` | test_tickets.py | Ticket creation succeeds, starts as "open" |
| T16 | `test_employee_cannot_create_ticket_for_other_department` | test_tickets.py | Cross-department ticket blocked |
| T17 | `test_employee_only_sees_own_tickets` | test_tickets.py | Ticket visibility scoping by role |
| T18 | `test_employee_cannot_change_ticket_status` | test_tickets.py | RBAC: only officer/admin can change status → 403 for employee |
| T19 | `test_officer_can_change_ticket_status` | test_tickets.py | Officer can add comment + change status |

Run with: `cd backend && pytest -v`

## Frontend component tests (Vitest + React Testing Library — `web/src/components/ui.test.jsx`)

| ID | Test | What it verifies |
|---|---|---|
| W01 | `StatusStamp` renders underscore-separated status as spaced text | Ticket status renders correctly (e.g. "in progress") |
| W02 | `StatusStamp` doesn't crash on an unrecognized status | Defensive rendering for unexpected data |
| W03 | `PriorityTag` renders the priority label | Priority badge shows the right text |
| W04 | `Button` fires its `onClick` handler | Basic interactivity |
| W05 | `Button` respects the `disabled` prop | Disabled state is reflected in the DOM |

Run with: `cd web && npm test`

## Manual / exploratory test cases

| ID | Area | Steps | Expected result |
|---|---|---|---|
| M01 | Document upload | Dept admin uploads a PDF with policy text | Document appears in list with chunk_count > 0; chatbot can answer from it |
| M02 | Low-confidence fallback | Ask a question unrelated to any uploaded document | Answer suggests raising a ticket; `suggest_ticket=true` |
| M03 | Ollama outage | Stop the Ollama container, ask a question | System still responds using the template fallback (no crash) |
| M04 | Ticket → resolution | Employee raises ticket from a weak chat answer, officer resolves it | `origin_chat_log_id` links back to the chat; status reaches Closed |
| M05 | Cross-role visibility | Officer from Dept A tries to view a ticket from Dept B via direct ticket ID | 404 (not visible), not a data leak |
| M06 | Audit trail | Dept admin uploads/deletes a document, officer changes ticket status | All 3 actions appear in Super Admin's Audit Log with correct actor/timestamp |
| M07 | Mobile app | Employee logs in on Expo app, asks a question, raises a ticket | Same behavior as web, on a phone-sized screen |
| M08 | Fresh clone | Clone repo on a machine with nothing installed, follow README exactly | `docker compose up` boots a fully working stack |

## Known gaps (documented, not silently skipped)

- Frontend component test coverage is intentionally shallow (shared UI primitives
  only) — page-level tests (Chat, Tickets, dashboards) are not yet written; see
  README "Known limitations".
- Embedding-model download requires internet access on first run; offline environments
  fall back to a weaker hashing embedder (by design, not a bug — see `architecture.md`).
