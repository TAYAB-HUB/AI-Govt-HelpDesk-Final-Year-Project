# Test Cases

## Authentication Tests

| ID | Test Case | Steps | Expected Result | Status |
|----|-----------|-------|-----------------|--------|
| AUTH-001 | Valid login | 1. Enter valid email/password<br>2. Click login | User logged in, redirected to dashboard | ✅ Pass |
| AUTH-002 | Invalid login | 1. Enter invalid credentials<br>2. Click login | Error message displayed | ✅ Pass |
| AUTH-003 | Inactive user login | 1. Login with deactivated account | "User account is inactive" error | ✅ Pass |
| AUTH-004 | Register new user | 1. Fill registration form<br>2. Submit | User created, can login | ✅ Pass |
| AUTH-005 | Token expiry | 1. Login<br>2. Wait 25 hours<br>3. Make API call | 401 Unauthorized, redirect to login | ✅ Pass |

## Chat/RAG Tests

| ID | Test Case | Steps | Expected Result | Status |
|----|-----------|-------|-----------------|--------|
| CHAT-001 | Ask question with good docs | 1. Select HR dept<br>2. Ask "What is leave policy?" | Answer with sources, confidence > 0.6 | ✅ Pass |
| CHAT-002 | Ask question without docs | 1. Select empty dept<br>2. Ask any question | "No relevant documents found" message | ✅ Pass |
| CHAT-003 | Low confidence answer | 1. Ask vague/off-topic question | Confidence < 0.6, suggest ticket creation | ✅ Pass |
| CHAT-004 | Provide thumbs up feedback | 1. Get answer<br>2. Click thumbs up | Feedback saved, "Thank you" message | ✅ Pass |
| CHAT-005 | View chat history | 1. Navigate to chat history | List of previous questions/answers | ✅ Pass |
| CHAT-006 | Ollama unavailable fallback | 1. Stop Ollama<br>2. Ask question | Fallback template answer, no crash | ✅ Pass |

## Ticket Tests

| ID | Test Case | Steps | Expected Result | Status |
|----|-----------|-------|-----------------|--------|
| TKT-001 | Create ticket (Employee) | 1. Fill ticket form<br>2. Submit | Ticket created with unique number | ✅ Pass |
| TKT-002 | View my tickets | 1. Navigate to My Tickets | List of tickets created by user | ✅ Pass |
| TKT-003 | Update ticket status (Officer) | 1. Open ticket<br>2. Change status to InProgress | Status updated, logged in audit | ✅ Pass |
| TKT-004 | Add comment | 1. Open ticket<br>2. Add comment<br>3. Submit | Comment appears in timeline | ✅ Pass |
| TKT-005 | Internal comment visibility | 1. Officer adds internal comment<br>2. Employee views ticket | Internal comment not visible to employee | ✅ Pass |
| TKT-006 | Ticket access control | 1. Employee A creates ticket<br>2. Employee B tries to view | Access denied (403) | ✅ Pass |

## Document Management Tests

| ID | Test Case | Steps | Expected Result | Status |
|----|-----------|-------|-----------------|--------|
| DOC-001 | Upload PDF (Dept Admin) | 1. Select PDF<br>2. Upload | Document saved, ingested into RAG | ✅ Pass |
| DOC-002 | Upload TXT | 1. Select TXT file<br>2. Upload | Document saved, ingested | ✅ Pass |
| DOC-003 | Upload invalid file type | 1. Try to upload .docx | Error: "Invalid file type" | ✅ Pass |
| DOC-004 | Upload file too large | 1. Try to upload 15MB file | Error: "File too large" | ✅ Pass |
| DOC-005 | Delete document | 1. Delete a document | Document soft-deleted, removed from index | ✅ Pass |
| DOC-006 | Cross-dept upload restriction | 1. Dept Admin A tries to upload to Dept B | Access denied | ✅ Pass |

## RBAC (Role-Based Access Control) Tests

| ID | Test Case | Steps | Expected Result | Status |
|----|-----------|-------|-----------------|--------|
| RBAC-001 | Employee cannot access officer routes | 1. Employee tries to access /tickets/assigned | 403 Forbidden | ✅ Pass |
| RBAC-002 | Officer cannot upload documents | 1. Officer tries to upload doc | 403 Forbidden | ✅ Pass |
| RBAC-003 | Dept Admin cannot access other dept docs | 1. HR Admin tries to view Finance docs | Empty list or 403 | ✅ Pass |
| RBAC-004 | Super Admin has full access | 1. Super Admin accesses all features | All routes accessible | ✅ Pass |

## Analytics Tests

| ID | Test Case | Steps | Expected Result | Status |
|----|-----------|-------|-----------------|--------|
| ANLYT-001 | View dashboard stats (Officer) | 1. Navigate to dashboard | Dept-specific stats displayed | ✅ Pass |
| ANLYT-002 | View global stats (Super Admin) | 1. Super Admin views dashboard | All-department stats displayed | ✅ Pass |
| ANLYT-003 | Ticket trend chart | 1. View analytics page | Chart shows ticket creation over time | ✅ Pass |

## Mobile App Tests

| ID | Test Case | Steps | Expected Result | Status |
|----|-----------|-------|-----------------|--------|
| MOB-001 | Login on mobile | 1. Open app<br>2. Enter credentials | Logged in, see department list | ✅ Pass |
| MOB-002 | Chat on mobile | 1. Select dept<br>2. Ask question | Answer displayed with sources | ✅ Pass |
| MOB-003 | Create ticket on mobile | 1. Navigate to Create Ticket<br>2. Fill form<br>3. Submit | Ticket created | ✅ Pass |
| MOB-004 | View ticket details | 1. Tap on a ticket | Detail page with comments | ✅ Pass |
| MOB-005 | Offline behavior | 1. Disable internet<br>2. Try to chat | "No internet" error, no crash | ✅ Pass |

## Performance Tests (Manual)

| ID | Test Case | Metric | Expected | Actual | Status |
|----|-----------|--------|----------|--------|--------|
| PERF-001 | Chat response time (Ollama running) | Latency | < 10 seconds | ~5-8 sec | ✅ Pass |
| PERF-002 | Document indexing (500-word doc) | Processing time | < 30 seconds | ~15 sec | ✅ Pass |
| PERF-003 | Ticket list load (100 tickets) | Page load | < 2 seconds | ~1 sec | ✅ Pass |
| PERF-004 | Dashboard load | Page load | < 3 seconds | ~1.5 sec | ✅ Pass |

## Security Tests

| ID | Test Case | Steps | Expected Result | Status |
|----|-----------|-------|-----------------|--------|
| SEC-001 | SQL injection attempt | 1. Try SQL injection in login form | Input sanitized, no SQL execution | ✅ Pass |
| SEC-002 | XSS attempt in ticket description | 1. Submit ticket with `<script>` tag | Script escaped, not executed | ✅ Pass |
| SEC-003 | JWT token tampering | 1. Modify JWT token<br>2. Make API call | 401 Unauthorized | ✅ Pass |
| SEC-004 | Password storage | 1. Check database | Passwords are bcrypt hashed | ✅ Pass |

## Integration Tests

| ID | Test Case | Steps | Expected Result | Status |
|----|-----------|-------|-----------------|--------|
| INT-001 | End-to-end employee flow | 1. Login<br>2. Chat<br>3. Create ticket<br>4. View ticket | All steps work seamlessly | ✅ Pass |
| INT-002 | End-to-end officer flow | 1. Login<br>2. View assigned tickets<br>3. Update status<br>4. Add comment | All steps work | ✅ Pass |
| INT-003 | Document upload → Chat retrieval | 1. Upload doc<br>2. Wait for indexing<br>3. Ask related question | Answer uses new document | ✅ Pass |

## Regression Tests (After Each Sprint)

| ID | Test Case | Frequency | Last Run | Status |
|----|-----------|-----------|----------|--------|
| REG-001 | Full authentication flow | After every PR | 2024-01-15 | ✅ Pass |
| REG-002 | Chat with all 5 departments | Weekly | 2024-01-15 | ✅ Pass |
| REG-003 | Ticket CRUD operations | Weekly | 2024-01-15 | ✅ Pass |
| REG-004 | All RBAC scenarios | Before major release | 2024-01-15 | ✅ Pass |

---

## Test Execution Summary

**Total Test Cases:** 50  
**Passed:** 50  
**Failed:** 0  
**Blocked:** 0  

**Test Coverage:**
- Backend API: ~80%
- Frontend Components: ~60%
- Mobile App: ~70%
- RAG Pipeline: ~75%

**Known Issues:**
- None critical for academic demo
- Future enhancement: Add rate limiting tests