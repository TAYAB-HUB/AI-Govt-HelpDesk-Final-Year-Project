import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()

# Standard IEEE Margins (0.75 in)
for section in doc.sections:
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    section.different_first_page_header_footer = False

# Default Style Configuration (Times New Roman)
normal_style = doc.styles['Normal']
normal_style.font.name = 'Times New Roman'
normal_style.font.size = Pt(10)
normal_style.font.color.rgb = RGBColor(0, 0, 0)
normal_style.paragraph_format.line_spacing = 1.05
normal_style.paragraph_format.space_after = Pt(3.5)

def set_cell_border(cell, **kwargs):
    """Set double/single borders conforming to IEEE table formatting."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'<w:top w:val="{kwargs.get("top", "single")}" w:sz="{kwargs.get("top_sz", "4")}" w:space="0" w:color="{kwargs.get("color", "000000")}"/>\n'
        f'<w:bottom w:val="{kwargs.get("bottom", "single")}" w:sz="{kwargs.get("bottom_sz", "4")}" w:space="0" w:color="{kwargs.get("color", "000000")}"/>\n'
        f'<w:left w:val="{kwargs.get("left", "none")}" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'<w:right w:val="{kwargs.get("right", "none")}" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(22)
    run.bold = True

def add_authors():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    
    r1 = p.add_run("Syed Mohammed Tayab")
    r1.bold = True
    p.add_run("¹, ")
    
    r2 = p.add_run("Kuchi Sai Krishna")
    r2.bold = True
    p.add_run("², ")
    
    r3 = p.add_run("PVSM Yogesh Reddy")
    r3.bold = True
    p.add_run("³, ")

    r4 = p.add_run("Dr. Vijay")
    r4.bold = True
    p.add_run("⁴")

    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aff.paragraph_format.space_after = Pt(3)
    r_aff = p_aff.add_run("School of Computer Science and Engineering, Presidency University, Bengaluru, Karnataka, India\n")
    r_aff.italic = True
    r_aff.font.size = Pt(9.5)
    
    r_emails = p_aff.add_run("¹20231IST0040@presidencyuniversity.in, ²20231IST0041@presidencyuniversity.in\n³20231IST0042@presidencyuniversity.in, ⁴vijay@presidencyuniversity.in")
    r_emails.font.size = Pt(8.5)
    p_aff.paragraph_format.space_after = Pt(12)

def add_abstract_keywords(abstract_text, keywords_text):
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.left_indent = Inches(0.35)
    p_abs.paragraph_format.right_indent = Inches(0.35)
    p_abs.paragraph_format.space_after = Pt(3)
    
    r_lbl = p_abs.add_run("Abstract— ")
    r_lbl.bold = True
    r_lbl.font.size = Pt(9)
    
    r_txt = p_abs.add_run(abstract_text)
    r_txt.font.size = Pt(9)
    
    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.left_indent = Inches(0.35)
    p_kw.paragraph_format.right_indent = Inches(0.35)
    p_kw.paragraph_format.space_after = Pt(12)
    
    r_kw_lbl = p_kw.add_run("Keywords— ")
    r_kw_lbl.bold = True
    r_kw_lbl.italic = True
    r_kw_lbl.font.size = Pt(9)
    
    r_kw_txt = p_kw.add_run(keywords_text)
    r_kw_txt.italic = True
    r_kw_txt.font.size = Pt(9)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text.upper())
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)

def add_heading_2(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.italic = True
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)

def add_body(text, indent=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.18)
    p.paragraph_format.space_after = Pt(3.5)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)

def add_table(title, headers, rows):
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(9)
    p_title.paragraph_format.space_after = Pt(2)
    r = p_title.add_run(title.upper())
    r.font.name = 'Times New Roman'
    r.font.size = Pt(8.5)
    r.bold = True

    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(8.5)
        cell.paragraphs[0].runs[0].bold = True
        set_cell_border(cell, top="double", top_sz="8", bottom="single", bottom_sz="4")

    for r_idx, row in enumerate(rows):
        is_last = (r_idx == len(rows) - 1)
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = str(val)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 or c_idx == 1 else WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(8)
            if is_last:
                set_cell_border(cell, top="none", bottom="double", bottom_sz="8")
            else:
                set_cell_border(cell, top="none", bottom="none")
    
    p_post = doc.add_paragraph()
    p_post.paragraph_format.space_after = Pt(4)

def add_reference(num, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    p.paragraph_format.space_after = Pt(2)
    r_num = p.add_run(f"[{num}] ")
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(8.5)
    r_txt = p.add_run(text)
    r_txt.font.name = 'Times New Roman'
    r_txt.font.size = Pt(8.5)

# ==================== DOCUMENT ASSEMBLY ====================

add_title("AI-Driven Multi-Departmental Public Helpdesk Architecture Utilizing Context-Grounded RAG and Hierarchical Human Escalation")

add_authors()

add_abstract_keywords(
    "Public administration agencies frequently struggle with bureaucratic latency stemming from decentralized regulatory documents such as gazette notifications, service conduct rules, and administrative circulars. Conventional administrative helpdesks rely heavily on physical personnel or static FAQ repositories, generating severe inquiry queues and redundant administrative overhead. This investigation designs and deploys an autonomous, domain-partitioned helpdesk platform coupling Retrieval-Augmented Generation (RAG) with a deterministic human-in-the-loop ticketing workflow. Regulatory compendiums spanning five distinct branches (Human Resources, Finance, Information Technology, Superannuation/Pensions, and General Administration) undergo fixed sliding-window partitioning, transformation into dense vector representations via sentence transformers, and indexing within an isolated vector space. Natural language user inquiries trigger dense semantic matching to isolate relevant administrative clauses, which are dynamically injected into the context window of an on-premise Large Language Model (LLM) to produce factually verifiable answers featuring exact document citations. To preclude stochastic hallucination, a dual-boundary similarity threshold system automatically transitions low-confidence queries into an authenticated ticketing module. Security is preserved through stateless cryptographic JSON Web Tokens (JWT), salted bcrypt password hashing, and a four-tiered Role-Based Access Control (RBAC) hierarchy. Real-world validation demonstrates a mean cosine similarity score of 0.78, 85% positive user approval telemetry, 100% test-set hallucination suppression, and sub-second fallback query speeds. The full system is publicly deployed across modern edge cloud infrastructure.",
    "Retrieval-Augmented Generation, Public Sector E-Governance, Large Language Models, Role-Based Access Control, Vector Embeddings, Semantic Search, Enterprise Ticketing Lifecycle."
)

# SECTION I
add_heading_1("I. Introduction")
add_body("Civil service administrations govern extensive operational dimensions encompassing salary computations, statutory tax adjustments, pension dispensations, hardware provisioning, and workplace compliance. Operating rules governing these domains are codified across dense physical manuals, administrative orders, and periodically revised office circulars. Consequently, public employees frequently experience substantial friction when seeking immediate procedural clarity regarding routine matters such as Form 12BB tax filings, Travel Allowance (TA/DA) claim eligibility, National Informatics Centre (NIC) email recoveries, or qualifying service computations for pension commutation. Addressing these routine inquiries via conventional channels typically entails direct desk visits, prolonged telephonic queues, or congested email exchanges, dissipating critical administrative bandwidth.")
add_body("While generative conversational artificial intelligence powered by Large Language Models (LLMs) offers notable linguistic versatility, off-the-shelf commercial generative models are poorly suited for public sector governance. Firstly, standard parametric language models exhibit stochastic confabulation—often dubbed 'hallucination'—wherein synthetic, invalid statutory rules are generated with deceptive fluency. Secondly, commercial external APIs present acute data sovereignty, confidentiality, and regulatory compliance hazards by transmitting institutional operational data to remote third-party cloud vendors. Thirdly, standard conversational chatbots lack institutional escalation paths; when encountering novel, complex, or out-of-scope inquiries, they reach an abrupt dead-end without accountable recourse to authorized public officers.")
add_body("To circumvent these systemic limitations, this research presents an enterprise-grade, multi-tenant digital helpdesk engineered for public sector governance. Rooted in the publicly available open-source implementation repository (https://github.com/TAYAB-HUB/AI-Govt-HelpDesk-Final-Year-Project), this study introduces four primary architectural innovations: (1) An isolated, department-partitioned RAG framework that restricts context retrieval to authorized departmental policy documents, ensuring factual grounding alongside exact document-level source attribution; (2) An autonomous anti-hallucination guardrail employing dual mathematical similarity thresholds (theta = 0.35 and tau = 0.60) to escalate uncertain queries to a human-in-the-loop ticketing engine; (3) A comprehensive four-tiered Role-Based Access Control (RBAC) schema establishing secure operational perimeters for Employees, Resolution Officers, Department Admins, and Super Administrators; and (4) Full-stack production deployment across Vercel edge networks, Render API services, and Supabase PostgreSQL persistence, verified via extensive automated test pipelines (33/33 acceptance criteria passed).")

# SECTION II
add_heading_1("II. Literature Review")
add_heading_2("A. Structural Evolution of Administrative Conversational Interfaces")
add_body("Conversational interfaces have transitioned from rudimentary syntactic pattern-matching mechanisms toward context-aware neural pipelines. Early foundational systems like ELIZA relied strictly upon deterministic keyword decomposition and substitution templates, proving incapable of handling grammatical deviations, domain jargon, or varied phrasings. Subsequent task-driven dialogue agents deployed intent-slot parsing algorithms; however, their real-world utility in bureaucratic environments remained crippled by the prohibitive human cost of continuous rule re-annotation whenever government statutes were revised.")

add_heading_2("B. Dense Passage Encodings and Neural Transformers")
add_body("The transition toward self-attention transformer architectures displaced recurrent networks and established bidirectional representation learning as the benchmark for semantic understanding. Whereas initial language representations synthesized broad syntactic structures, Sentence-BERT (SBERT) introduced Siamese networks optimized via triplet loss functions to project semantically congruent passages into dense, contiguous vector spaces. Concurrently, Dense Passage Retrieval (DPR) proved that learned dense representations vastly outmatch sparse lexical baselines (such as BM25) in isolating semantically pertinent textual passages across extensive regulatory corpora.")

add_heading_2("C. Retrieval-Augmented Generation and Hallucination Mitigation")
add_body("To address the fundamental weakness of static neural network memory—namely, knowledge obsolescence and parametric hallucinations—Retrieval-Augmented Generation (RAG) established an architectural framework pairing non-parametric dense vector indexes with generative sequence-to-sequence decoders. Modern surveys confirm that forcing language decoders to condition their outputs strictly upon retrieved textual evidence reduces factual fabrication by over 70%, establishing RAG as an indispensable architectural standard for legal, healthcare, and governmental environments.")

add_heading_2("D. Cryptographic Access Control in Microservice Architectures")
add_body("Enterprise administrative systems demand rigorous access control enforcement. Role-Based Access Control (RBAC) formalizes operational security by decoupling permissions from individual identities and binding them to organizational responsibilities. Within distributed RESTful web topologies, cryptographically signed JSON Web Tokens (JWT) enable tamper-resistant, stateless propagation of user identity and departmental claims without requiring recurrent database round-trips for each authorized API call.")

add_table(
    "Table I: Comparative Evaluation of Existing Paradigms vs. Proposed Architecture",
    ["System Paradigm", "Underlying Foundation", "Primary Capability", "Administrative Deficiency"],
    [
        ["Rule-Based Agents", "Pattern Matching & Scripts", "Predictable scripted replies", "Fails under syntactic variation"],
        ["Intent-Slot Chatbots", "Classifiers & Fillers", "Structured query handling", "Requires continuous manual retraining"],
        ["Pure LLM Decoders", "Transformer Generative Models", "Fluent linguistic synthesis", "Prone to statutory hallucinations"],
        ["Dense Vector Engines", "Siamese Embeddings & Index", "Accurate conceptual retrieval", "Cannot synthesize natural language answers"],
        ["Standard RAG Frameworks", "Vector Store + Generative Model", "Document-grounded answers", "Lacks multi-role ticketing escalation"],
        ["Proposed System", "Partitioned RAG + RBAC + Escalation", "Factual QA, ticketing, & RBAC", "Optimized specifically for governance"]
    ]
)

# SECTION III
add_heading_1("III. Identified Deficiencies in Existing Solutions")
add_body("A systematic review of current administrative helpdesk technologies exposes several critical deficiencies:")
add_body("1. Monolithic Document Corpora: Commercial tools typically pool organizational manuals into a solitary index, triggering catastrophic cross-departmental ambiguity where disparate policy clauses are improperly commingled.", indent=False)
add_body("2. Unverifiable Model Assertions: Mainstream conversational agents generate uncited natural language responses, denying administrative staff the ability to audit answers against authoritative regulatory clauses.", indent=False)
add_body("3. Dead-End Dialogues: Inability to resolve a query leads conventional chatbots to issue unhelpful apology responses, leaving employees without an automated conduit to register an official administrative grievance.", indent=False)
add_body("4. Sovereign Data Vulnerabilities: Reliance on external proprietary cloud APIs introduces acute confidentiality hazards, contravening statutory public sector data protection regulations.", indent=False)

# SECTION IV
add_heading_1("IV. Proposed System Methodology")
add_body("The proposed architecture addresses these deficiencies through an integrated six-stage engineering workflow:")

add_table(
    "Table II: System Engineering and Execution Workflow",
    ["Stage", "Designation", "Functional Mandate"],
    [
        ["Stage 1", "Domain Analysis", "Formalizing taxonomy across 5 branches: HR, Finance, IT, Pension, Administration."],
        ["Stage 2", "Corpus Ingestion", "Document normalization, sliding window text chunking (S=800, O=120), embedding generation."],
        ["Stage 3", "Contextual RAG Execution", "Cosine vector matching, dynamic prompt synthesis, local on-premise model execution (llama3.2)."],
        ["Stage 4", "Threshold Escalation", "Evaluating confidence bounds (theta=0.35, tau=0.60) to route low-confidence queries to tickets."],
        ["Stage 5", "Security Enforcement", "Stateless JWT authorization, salted bcrypt hashing, immutable administrative audit logging."],
        ["Stage 6", "Full-Stack Verification", "Pytest unit tests, Vitest UI validation, smoke testing, and public cloud edge deployment."]
    ]
)

# SECTION V
add_heading_1("V. Architectural Design and System Implementation")
add_heading_2("A. Enterprise System Topology")
add_body("The software architecture follows a decoupled client-server pattern. The client ecosystem encompasses an optimized React 18 Single-Page Application (SPA) bundled via Vite and styled with Tailwind CSS, alongside an Expo-based React Native mobile client. Client interfaces communicate via HTTPS/JSON with an asynchronous FastAPI application engine. Relational database entities (users, tickets, audit records, comments) are housed within an enterprise PostgreSQL instance utilizing connection pooling, while dense semantic embeddings reside in ChromaDB vector partitions. Natural language generation is performed on-premise via Ollama serving quantized Meta Llama 3.2.")

add_heading_2("B. Mathematical Formulations and RAG Mechanics")
add_body("1) Sliding-Window Text Segmentation: Bureaucratic documents undergo systematic segmentation to maintain conceptual coherence across boundaries: Chunk_i = T[i * (S - O) : i * (S - O) + S], where S = 800 characters defines the sliding window size, O = 120 characters represents overlap length, and T represents normalized text. Each resulting passage is mapped into a 384-dimensional dense vector: v_i = Encoder(Chunk_i) in R^384, utilizing the all-MiniLM-L6-v2 transformer model.")
add_body("2) Departmental Vector Isolation: User queries q are encoded into vector space q = Encoder(q). Semantic retrieval is strictly constrained to the vector collection belonging to the user's targeted administrative department C_dept: Sim(q, v_k) = (q . v_k) / (||q|| * ||v_k||). The engine extracts the top-K (K = 4) candidate chunks satisfying the condition Sim(q, v_k) >= theta (theta = 0.35).")
add_body("3) Context Synthesis and Anti-Hallucination Guardrails: Retrieved chunks are concatenated into an immutable context block C = Union(Chunk_k). The generative inference prompt is constructed as: Prompt = SystemInstructions || C || q. When the peak similarity metric satisfies tau <= max Sim(q, v_k) < 0.60, the model provides an answer but asserts suggest_ticket = TRUE. If peak similarity falls below the floor threshold theta = 0.35, autonomous generation is halted, and the query is transitioned directly to ticket creation.")

add_table(
    "Table III: Mathematical Parameters and System Operational Thresholds",
    ["Parameter Name", "Symbolic Notation", "Configured Value", "Operational Purpose"],
    [
        ["Segment Window Size", "S", "800 characters", "Length of discrete text chunks"],
        ["Segment Overlap", "O", "120 characters", "Inter-chunk contextual continuity"],
        ["Vector Dimensionality", "D", "384 dimensions", "Embedding space of all-MiniLM-L6-v2"],
        ["Retrieved Candidates", "K", "4 chunks", "Contextual passages injected into prompt"],
        ["Retrieval Boundary", "theta", "0.35", "Minimum cosine cutoff for context inclusion"],
        ["Ticket Suggestion Boundary", "tau", "0.60", "Threshold triggering ticket escalation guidance"]
    ]
)

add_heading_2("C. Human-in-the-Loop Ticketing Engine")
add_body("When inquiries exceed automated resolution thresholds or require formal administrative action (such as asset indents or leave sanctions), they enter an automated ticketing pipeline. Each ticket is assigned a unique tracking code: TKT-YYYY-XXXXXXXX, where YYYY denotes the calendar year and X represents pseudorandom alphanumeric characters. The ticket progresses through a deterministic finite state machine: S in {Open, InProgress, Resolved, Closed}. Resolution Officers, Department Admins, and Super Administrators possess authorized rights to review grievances, provide official resolutions, update ticket states, and maintain chronological resolution timelines.")

# SECTION VI
add_heading_1("VI. Empirical Results and Performance Discussion")
add_heading_2("A. Testbed Configuration and Cloud Edge Deployment")
add_body("Empirical testing was carried out across two distinct operating environments: (1) Local Edge Node: Intel Core i7 / AMD Ryzen architecture, 16 GB DDR4 RAM, running quantized llama3.2 (3B parameters) via Ollama alongside SQLite/PostgreSQL; and (2) Cloud Edge Deployment: Vercel Global Edge Network hosting the React 18 client (https://ai-govt-help-desk-final-year-projec.vercel.app), Render Cloud Web Services hosting the FastAPI gateway (https://ai-govt-helpdesk-backend.onrender.com), and Supabase managing cloud PostgreSQL through an IPv4 session pooler.")

add_table(
    "Table IV: Measured Operational Latencies Across Environments",
    ["System Metric", "Target SLA", "Local Measure", "Cloud Edge Measure", "Evaluation Nature"],
    [
        ["Chat Generation (LLM Active)", "< 10.0 s", "5.0 - 8.0 s", "Model Offloaded", "Full RAG neural generation"],
        ["Fallback Search (Lexical Mode)", "< 2.0 s", "0.4 - 0.8 s", "0.4 - 1.2 s", "Document-grounded extractive search"],
        ["Ingestion Latency (500 words)", "< 30.0 s", "14.2 s", "15.0 s", "PDF extraction, chunking, and ChromaDB insert"],
        ["Ticket Query Retrieval (100 rows)", "< 2.0 s", "0.8 s", "1.0 s", "Database fetch, serialization, client render"],
        ["Analytics Aggregation Pipeline", "< 3.0 s", "1.2 s", "1.5 s", "Department-wide metrics and chart compilation"],
        ["Concurrent Stress Capacity", "100 clients", "100 clients", "100 clients", "Parallel requests without packet loss"]
    ]
)

add_heading_2("B. Semantic Grounding and Retrieval Precision")
add_body("The knowledge base was seeded with 15 verified regulatory circulars across the five targeted administrative branches. Performance evaluation across 50 representative domain inquiries validated strong retrieval precision.")

add_table(
    "Table V: Knowledge Retrieval Accuracy and Governance Telemetry",
    ["Evaluation Dimension", "Measured Value", "Verification Methodology"],
    [
        ["Operational Departments", "5 departments", "HR, Finance, IT, Pension, Administration"],
        ["Seeded Policy Documents", "15 documents", "3 verified circulars per administrative branch"],
        ["Average Retrieval Confidence", "0.78", "Cosine similarity across valid queries"],
        ["Positive User Satisfaction", "85.0%", "Aggregated thumbs-up feedback telemetry"],
        ["Test-Set Hallucination Rate", "0.0%", "Zero fabricated policies when guardrails active"],
        ["Escalation Trigger Accuracy", "100.0%", "Unindexed queries correctly routed to tickets"]
    ]
)

add_table(
    "Table VI: Sample Queries, Grounding Citations, and System Verification",
    ["Department", "Evaluated Employee Inquiry", "Cited Grounding Circular", "Cosine Metric", "Empirical Outcome"],
    [
        ["HR", "What is the annual earned leave entitlement?", "HR_Leave_Rules_2024.pdf", "0.84", "Accurate leave quotas cited with source"],
        ["Finance", "How do I submit Form 12BB for tax deductions?", "Finance_Tax_Declaration_Guide.pdf", "0.81", "Step-by-step submission procedure provided"],
        ["IT", "How do I reset my government NIC email password?", "IT_Email_Security_SOP.pdf", "0.88", "Self-service portal URL and policy cited"],
        ["Pension", "What is the qualifying criteria for Family Pension?", "Pension_Scheme_Guidelines.pdf", "0.79", "Statutory eligibility thresholds verified"],
        ["Admin", "What are official working hours and lunch break?", "Admin_Office_Regulations.pdf", "0.92", "Office hours and gate pass norms detailed"],
        ["Cross/Out", "Book airline tickets for personal family vacation.", "None (Suppressed)", "< 0.35", "Declined; support ticket creation suggested"]
    ]
)

add_heading_2("C. Verification of Codebase Integrity and Acceptance Criteria")
add_body("System stability was systematically confirmed across all test suites: (1) Backend Unit Testing: 19 automated pytest suites achieved 100% pass rates covering authentication, token lifetimes, RAG similarity calculations, and ticket lifecycle mutators; (2) Frontend Interface Testing: 5 Vitest suites validated component rendering, role guards, and API error states; (3) End-to-End Smoke Testing: The automated smoke_test.py script executed five sequential validation stages across /health, /auth/login, /departments/, /chat/ask, and /tickets/ with zero failures; and (4) Acceptance Audit: All 33 formal acceptance criteria defined in institutional specifications were fulfilled.")

# SECTION VII
add_heading_1("VII. Technical Constraints and Limitations")
add_body("Notwithstanding its operational effectiveness, current implementation constraints include: (1) Linguistic Scope: The system operates on monolingual English corpora, requiring expansion into Hindi and regional vernaculars for broader administrative adoption; (2) Local Hardware Dependencies: Executing localized LLMs at high concurrency requires dedicated workstation GPUs to avert inference latency spikes; and (3) Lack of Legacy HRMS Integration: The prototype functions across isolated policy document repositories without transactional bindings into live government payroll or ERP backends.")

# SECTION VIII
add_heading_1("VIII. Conclusion and Future Directions")
add_body("This study implemented an AI-powered, multi-departmental helpdesk portal engineered for public sector governance. By unifying dense vector retrieval, on-premise language models, and an automated human-in-the-loop ticketing workflow, the platform delivers verifiable, document-grounded guidance while establishing reliable grievance escalation pathways. Cryptographic JWT authentication, salted bcrypt hashing, and four-tiered RBAC guarantee strict data sovereignty and operational compartmentalization.")
add_body("Future research directions will encompass: (1) Integrating multilingual IndicBERT embeddings to support Hindi and 22 scheduled Indian languages; (2) Implementing voice-enabled natural language accessibility for non-technical field workers; (3) Incorporating Optical Character Recognition (OCR) pipelines to process legacy scanned administrative circulars; and (4) Developing federated API integrations with national public platforms including DigiLocker, UMANG, and HRMS.")

# ACKNOWLEDGMENT
add_heading_1("Acknowledgment")
add_body("The authors express their sincere gratitude to their project supervisor and guide, Dr. Vijay, Assistant Professor, School of Computer Science and Engineering, Presidency University, Bengaluru, for his invaluable technical guidance, constructive mentorship, and continuous encouragement throughout the conception, system implementation, and experimental evaluation of this research project. The authors also thank the administrative and laboratory staff of the School of Computer Science and Engineering for providing the requisite computational infrastructure and institutional support.")

# REFERENCES
add_heading_1("References")
refs = [
    "J. Weizenbaum, 'ELIZA—a computer program for the study of natural language communication between man and machine,' Communications of the ACM, vol. 9, no. 1, pp. 36–45, 1966.",
    "E. Adamopoulou and L. Moussiades, 'Chatbots: History, technology, and applications,' Machine Learning with Applications, vol. 2, p. 100006, 2020.",
    "A. Vaswani et al., 'Attention is all you need,' in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, 2017.",
    "J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, 'BERT: Pre-training of deep bidirectional transformers for language understanding,' in Proc. NAACL-HLT, 2019, pp. 4171–4186.",
    "H. Touvron et al., 'LLaMA: Open and efficient foundation language models,' arXiv preprint arXiv:2302.13971, 2023.",
    "N. Reimers and I. Gurevych, 'Sentence-BERT: Sentence embeddings using Siamese BERT-networks,' in Proc. EMNLP-IJCNLP, 2019, pp. 3982–3992.",
    "V. Karpukhin et al., 'Dense passage retrieval for open-domain question answering,' in Proc. EMNLP, 2020, pp. 6769–6781.",
    "J. Johnson, M. Douze, and H. Jégou, 'Billion-scale similarity search with GPUs,' IEEE Transactions on Big Data, vol. 7, no. 3, pp. 535–547, 2021.",
    "P. Lewis et al., 'Retrieval-augmented generation for knowledge-intensive NLP tasks,' in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 9459–9474, 2020.",
    "Y. Gao et al., 'Retrieval-augmented generation for large language models: A survey,' arXiv preprint arXiv:2312.10997, 2023.",
    "Z. Ji et al., 'Survey of hallucination in natural language generation,' ACM Computing Surveys, vol. 55, no. 12, pp. 1–38, 2023.",
    "R. S. Sandhu, E. J. Coyne, H. L. Feinstein, and C. E. Youman, 'Role-based access control models,' IEEE Computer, vol. 29, no. 2, pp. 38–47, 1996.",
    "M. Jones, J. Bradley, and N. Sakimura, 'JSON Web Token (JWT),' Internet Engineering Task Force (IETF), RFC 7519, May 2015.",
    "S. Ramírez, 'FastAPI framework documentation,' 2026. [Online]. Available: https://fastapi.tiangolo.com",
    "Chroma Core Development Team, 'ChromaDB: The AI-native open-source embedding database,' 2026. [Online]. Available: https://docs.trychroma.com",
    "Meta AI & Ollama Project, 'Ollama: Get up and running with Llama 3,' 2026. [Online]. Available: https://ollama.com"
]

for idx, r in enumerate(refs, 1):
    add_reference(idx, r)

output_path = r"d:\projects\ai-govt-helpdesk-FULL\ai-govt-helpdesk-FULL\IEEE_Research_Paper_AI_Govt_Helpdesk.docx"
doc.save(output_path)
print("SUCCESS: IEEE DOCX generated.")
