# User Manual

Demo logins (all use password `Demo@1234` — see README for the full list).

## Employee

1. **Log in** at the web app (or the Expo mobile app) with your employee account.
2. **Ask a question** on the Chat page. Pick your department if you belong to more
   than one context, type your question, and submit.
3. Read the **answer** — every answer shows the source document(s) it was
   grounded on, with a short snippet and a relevance score.
4. If the answer is weak (low similarity) the system will suggest **raising a
   ticket** — click through to pre-fill a ticket from that chat.
5. Use **thumbs up/down** on any answer to give feedback.
6. Go to **My Tickets** to see all tickets you've raised and their status
   (Open → In Progress → Resolved → Closed), with the full comment timeline.

## Department Officer

1. Log in and go to **Assigned Tickets** (or your department's ticket queue).
2. Open a ticket to see the employee's question/description and any prior
   comments.
3. Add a **comment** to respond, and optionally change the **status**
   (In Progress / Resolved / Closed) — employees cannot change status
   themselves, only officers/admins can.

## Department Admin

1. **Documents**: upload PDF/TXT/MD files for your department — they are
   automatically chunked and embedded for the chatbot to use. Delete
   outdated documents from the same page.
2. **Officers**: view officers/employees in your department.
3. **Analytics**: see tickets by status/category and the most common
   employee questions for your department.
4. **Tickets**: assign unassigned tickets to a specific officer.

## Super Admin

Everything a Department Admin can do, across **all** departments, plus:

1. **Departments**: create new departments.
2. **Users**: change any user's role, enable/disable accounts.
3. **Audit Log**: view a full history of sensitive actions (document
   uploads, ticket status changes, user management) with actor and
   timestamp.
4. **Global analytics**: aggregate view across every department.

## Common workflow (Definition of Success)

Employee logs in → asks a question → gets a source-cited answer → (if
unresolved) raises a ticket → officer picks it up and updates status → ticket
reaches Closed. This end-to-end path is what Review 4 / the viva will most
likely be demoed against.
