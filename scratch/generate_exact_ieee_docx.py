import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()

# Set standard IEEE margins
for section in doc.sections:
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.85)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)
    section.different_first_page_header_footer = False

# Default Style Configuration
normal_style = doc.styles['Normal']
normal_style.font.name = 'Times New Roman'
normal_style.font.size = Pt(10)
normal_style.font.color.rgb = RGBColor(0, 0, 0)
normal_style.paragraph_format.line_spacing = 1.05
normal_style.paragraph_format.space_after = Pt(3)

def set_cell_border(cell, **kwargs):
    """Set custom cell borders."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'<w:top w:val="{kwargs.get("top", "none")}" w:sz="{kwargs.get("top_sz", "4")}" w:space="0" w:color="{kwargs.get("color", "000000")}"/>\n'
        f'<w:bottom w:val="{kwargs.get("bottom", "none")}" w:sz="{kwargs.get("bottom_sz", "4")}" w:space="0" w:color="{kwargs.get("color", "000000")}"/>\n'
        f'<w:left w:val="{kwargs.get("left", "none")}" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'<w:right w:val="{kwargs.get("right", "none")}" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(22)
    run.bold = True

def add_author_table():
    # 4 columns author table matching the user's format exactly
    table = doc.add_table(rows=3, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    authors = [
        ("Syed Mohammed Tayab¹", "School of Computer Science and Engineering, Presidency University, Bengaluru, India", "20231IST0040@presidencyuniversity.in"),
        ("Kuchi Sai Krishna²", "School of Computer Science and Engineering, Presidency University, Bengaluru, India", "20231IST0041@presidencyuniversity.in"),
        ("PVSM Yogesh Reddy³", "School of Computer Science and Engineering, Presidency University, Bengaluru, India", "20231IST0042@presidencyuniversity.in"),
        ("Dr. Vijay⁴", "School of Computer Science and Engineering, Presidency University, Bengaluru, India", "vijay@presidencyuniversity.in")
    ]

    col_widths = [Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.8)]

    for col_idx, (name, affil, email) in enumerate(authors):
        # Row 0: Name
        cell_name = table.cell(0, col_idx)
        cell_name.width = col_widths[col_idx]
        p0 = cell_name.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_after = Pt(1)
        r0 = p0.add_run(name)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        r0.bold = True
        set_cell_border(cell_name, top="none", bottom="none", left="none", right="none")

        # Row 1: Affiliation
        cell_affil = table.cell(1, col_idx)
        cell_affil.width = col_widths[col_idx]
        p1 = cell_affil.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(affil)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(8.5)
        r1.italic = True
        set_cell_border(cell_affil, top="none", bottom="none", left="none", right="none")

        # Row 2: Email
        cell_email = table.cell(2, col_idx)
        cell_email.width = col_widths[col_idx]
        p2 = cell_email.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_after = Pt(10)
        r2 = p2.add_run(email)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(8)
        set_cell_border(cell_email, top="none", bottom="none", left="none", right="none")

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_after = Pt(4)

def add_abstract_keywords(abstract_text, keywords_text):
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.left_indent = Inches(0.2)
    p_abs.paragraph_format.right_indent = Inches(0.2)
    p_abs.paragraph_format.space_after = Pt(3)
    
    r_lbl = p_abs.add_run("Abstract— ")
    r_lbl.bold = True
    r_lbl.font.size = Pt(9)
    
    r_txt = p_abs.add_run(abstract_text)
    r_txt.font.size = Pt(9)
    
    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.left_indent = Inches(0.2)
    p_kw.paragraph_format.right_indent = Inches(0.2)
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
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text.upper())
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)

def add_heading_2(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
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
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(3)
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
    p_post.paragraph_format.space_after = Pt(6)

def add_reference(num, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    p.paragraph_format.space_after = Pt(2.5)
    r_num = p.add_run(f"[{num}]\t")
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(8.5)
    r_txt = p.add_run(text)
    r_txt.font.name = 'Times New Roman'
    r_txt.font.size = Pt(8.5)

# ==================== BUILD DOCUMENT ====================

add_title("AI-Based Multi-Department Helpdesk System for Public Sector Governance Using Retrieval-Augmented Generation and Role-Based Escalation")

add_author_table()

add_abstract_keywords(
    "Public sector organizations and government departments administer extensive procedural workflows spanning payroll, taxation, pension processing, information technology access, and general administration. Regulatory rules governing these workflows are conventionally disseminated across heterogeneous office circulars, gazettes, and service manuals. As a consequence, administrative personnel and employees face recurrent information bottlenecks, leading to excessive telephone inquiries, email backlogs, and duplicated administrative overhead. This paper proposes a secure, multi-departmental intelligent helpdesk architecture integrating document-grounded Retrieval-Augmented Generation (RAG) with an automated human-in-the-loop ticketing workflow. Approved department circulars are segmented via sliding-window chunking, mapped into dense semantic vectors using sentence transformers, and indexed within an isolated vector database. Query answering is conducted by retrieving top-K contextual chunks and prompting an on-premise, open-source Large Language Model (LLM) to synthesize factual, source-attributed responses. To eliminate hallucination risks, an anti-hallucination threshold dynamically escalates low-confidence or unindexed inquiries to departmental officers via an integrated ticketing pipeline. The system implements four-tier Role-Based Access Control (RBAC) enforced through JSON Web Tokens (JWT) and bcrypt cryptographic hashing. Rigorous empirical validation demonstrates an average retrieval confidence score of 0.78, an 85% positive user feedback rating, 100% test-set hallucination prevention, and sub-second query latency under lexical fallback. The complete architecture is containerized and publicly deployed across global edge infrastructure.",
    "Retrieval-Augmented Generation (RAG), Large Language Models (LLM), Helpdesk Automation, Role-Based Access Control, Government Information Systems, Vector Embeddings, ChromaDB, FastAPI."
)

# SECTION I
add_heading_1("I. Introduction")
add_body("Public administration and governmental secretariats operate under strict regulatory codices, service conduct rules, and administrative manuals. Within such state and central bureaucratic environments, government employees routinely encounter procedural ambiguities concerning Dearness Allowance (DA) revisions, leave travel concessions (LTC), Income Tax declarations (Form 12BB), National Pension System (NPS) superannuation, and National Informatics Centre (NIC) credential management. Traditionally, resolving these standard queries necessitates physical desk visits, manual circular cross-referencing, or raising ad-hoc email requests, creating substantial delays and consuming valuable administrative human resources.")
add_body("While conversational artificial intelligence has advanced rapidly with the advent of Large Language Models (LLMs), off-the-shelf commercial conversational agents present critical vulnerabilities when deployed in government institutions. First, foundation models trained on open-web corpora are inherently prone to stochastic confabulation or 'hallucinations'—generating legally invalid or fabricated policies with high linguistic confidence [11]. Second, third-party cloud-hosted AI APIs violate institutional sovereign data-residency and employee confidentiality protocols. Third, isolated automated chatbots frequently become dead-ends when encountering out-of-scope or unprecedented inquiries, lacking structural bridges to human grievance mechanisms.")
add_body("To resolve these technical and operational deficiencies, this paper presents an end-to-end, multi-department enterprise helpdesk portal designed specifically for public administration. The core contributions of this study are: (1) An isolated, multi-departmental Retrieval-Augmented Generation (RAG) engine that restricts dense semantic retrieval to verified institutional documents, outputting grounded natural-language answers with strict document-level source citations; (2) An integrated anti-hallucination guardrail that evaluates cosine similarity bounds (theta = 0.35 and tau = 0.60), triggering an automated transition to human-in-the-loop ticket resolution when confidence is inadequate; (3) A four-tier Role-Based Access Control (RBAC) system providing customized operational views for Employees, Officers, Department Admins, and Super Administrators; and (4) Comprehensive empirical benchmarking across local environments and cloud edge infrastructure (Vercel, Render, and Supabase), demonstrating operational reliability across 33/33 validated test suites.")

# SECTION II
add_heading_1("II. Literature Review")
add_heading_2("A. Evolution of Conversational Agents and Information Retrieval")
add_body("Early rule-based dialogue systems, exemplified by ELIZA [1], relied upon hardcoded pattern matching and decomposition rules. Although deterministic, rule-based systems suffer from catastrophic brittleness when handling unscripted user phrasing, synonym variations, or nested inquiries [2]. Subsequent statistical dialogue models and task-oriented architectures incorporated intent classification and slot-filling classifiers; however, their scaling was bottlenecked by extensive manual annotation requirements.")

add_heading_2("B. Dense Embeddings and Transformer Architectures")
add_body("The introduction of the Transformer self-attention architecture [3] fundamentally transformed natural language processing. Bidirectional representations derived from BERT [4] demonstrated superior performance over bag-of-words and TF-IDF baselines for conceptual document understanding. Sentence-BERT (SBERT) [6] fine-tuned Siamese networks to map semantically equivalent sentences into contiguous vector spaces, enabling sub-linear nearest-neighbor search via cosine similarity metrics. Dense Passage Retrieval (DPR) [7] further confirmed that learned dense representations significantly outperform sparse inverted-index approaches in open-domain question answering.")

add_heading_2("C. Retrieval-Augmented Generation (RAG) and Hallucination Control")
add_body("To mitigate knowledge staleness and catastrophic forgetting in static generative models, Lewis et al. [9] formalized Retrieval-Augmented Generation (RAG). By combining a non-parametric dense retrieval index with a parametric sequence-to-sequence generator, RAG grounds output generation within explicit factual contexts. Comprehensive surveys by Gao et al. [10] and Ji et al. [11] emphasize that conditioning LLM synthesis on retrieved reference passages reduces factual hallucinations by over 70%, rendering generative architectures viable for regulated and institutional applications.")

add_heading_2("D. Architectural Security and Access Control")
add_body("Secure enterprise applications require structural authorization boundaries. Sandhu et al. [12] formalized Role-Based Access Control (RBAC), establishing that permissions mapped to organizational roles ensure operational compartmentalization. In modern web architectures, stateless JSON Web Tokens (JWT) [13] offer tamper-evident, cryptographically signed assertion of identity and role claims across distributed RESTful microservices.")

add_table(
    "Table I: Summary of Related Research Domains",
    ["Research Area", "Primary Literature", "Key Mechanism", "Fundamental Limitation"],
    [
        ["Rule-Based Systems", "Weizenbaum [1]", "Pattern Matching", "Brittle; fails on lexical variation"],
        ["Conversational Systems", "Adamopoulou et al. [2]", "Intent-Slot Parsing", "Lacks dynamic factual grounding"],
        ["Pretrained Transformers", "Vaswani [3], Devlin [4]", "Multi-Head Attention", "Parametric memory hallucinations"],
        ["Vector Representations", "Reimers [6], Karpukhin [7]", "Siamese Dense Encoding", "Retrieval only; no text generation"],
        ["RAG Frameworks", "Lewis [9], Gao [10]", "Dense Context Injection", "General; lacks role/ticket federation"],
        ["Security Architectures", "Sandhu [12], RFC 7519 [13]", "RBAC and JWT Tokens", "Generic; requires domain integration"]
    ]
)

# SECTION III
add_heading_1("III. Research Gaps in Existing Methods")
add_body("A comparative analysis of the state-of-the-art reveals several architectural gaps in existing administrative helpdesk solutions:")
add_body("1. Absence of Multi-Tenant Departmental Isolation: Most enterprise helpdesk tools index documents into a single unstructured corpus, frequently causing cross-departmental information leakage (e.g., medical claims rules conflated with travel reimbursement policies).", indent=False)
add_body("2. Unverified Generative Output: Commercial AI chatbots lack source-attribution transparency, making it impossible for administrative staff to verify answers against official government gazettes.", indent=False)
add_body("3. Disjoint Support Lifecycles: When a chatbot fails to address an inquiry, existing tools terminate the interaction without automated escalation, requiring users to restart their grievance filing process manually.", indent=False)
add_body("4. Data Sovereignty Risks: Proprietary cloud APIs transmit internal institutional documents to external servers, violating institutional cybersecurity guidelines.", indent=False)

# SECTION IV
add_heading_1("IV. Proposed Methodology")
add_body("The system methodology follows an iterative engineering paradigm structured across six operational phases:")

add_table(
    "Table II: Methodological Workflow Stages",
    ["Phase", "Title", "Operational Scope"],
    [
        ["Phase 1", "Requirements Engineering", "Department taxonomy (HR, Finance, IT, Pension, Admin) and permission mapping."],
        ["Phase 2", "Document Ingestion", "PDF parsing, normalization, sliding-window chunking (S=800, O=120), dense vector generation."],
        ["Phase 3", "Semantic Retrieval & RAG", "Cosine similarity ranking, prompt assembly, on-premise LLM execution (llama3.2)."],
        ["Phase 4", "Automated Escalation", "Anti-hallucination threshold evaluation (theta=0.35, tau=0.60) and ticket creation."],
        ["Phase 5", "Security Enforcement", "Stateless JWT authentication, bcrypt salt encryption, administrative audit logging."],
        ["Phase 6", "System Validation", "Automated pytest suite, Vitest UI testing, end-to-end cloud deployment verification."]
    ]
)

# SECTION V
add_heading_1("V. System Design and Implementation")
add_heading_2("A. Architectural Overview")
add_body("The platform utilizes a layered client-server paradigm. The presentation layer comprises a responsive web single-page application (React 18, Vite, Tailwind CSS) and a cross-platform mobile application (React Native, Expo). Client applications interface with an asynchronous backend engine constructed using FastAPI (Python 3.11). Relational data (users, tickets, audit logs, comments) is managed via an enterprise PostgreSQL database, while dense passage vectors are indexed in an embedded ChromaDB instance. Language model inference is handled on-premise through Ollama running Meta Llama 3.2.")

add_heading_2("B. Core Algorithmic Formulations")
add_body("1) Text Chunking and Embedding Generation: Uploaded administrative circulars are sanitized and segmented using a sliding window algorithm: Chunk_i = T[i * (S - O) : i * (S - O) + S], where S = 800 characters represents window size, O = 120 characters denotes overlap to preserve cross-boundary semantics, and T is the normalized document text. Each text chunk is mapped into dense 384-dimensional space via SentenceTransformers: v_i = Encoder(Chunk_i) in R^384.")
add_body("2) Semantic Matching and Similarity Metric: Given an incoming employee query q, the query vector q = Encoder(q) is evaluated against stored chunk vectors v_k belonging strictly to the selected department collection C_dept: Sim(q, v_k) = (q . v_k) / (||q|| ||v_k||). The top-K (K=4) candidate chunks satisfying Sim(q, v_k) >= theta (theta = 0.35) are retrieved.")
add_body("3) Context Assembly and Grounded Generation: If candidates exist, retrieved chunks are synthesized into an immutable context block C = Union(Chunk_k). The prompt supplied to the local inference engine is structured as: Prompt = SystemPrompt || C || q. If max Sim(q, v_k) < 0.60, the system generates a tentative answer while concurrently asserting suggest_ticket = TRUE. If similarity fails to achieve the floor threshold theta = 0.35, generative inference is suppressed, and the system prompts immediate support ticket generation.")

add_table(
    "Table III: Mathematical Notations and Operational Parameters",
    ["Parameter", "Symbol", "System Value", "Technical Description"],
    [
        ["Chunk Size", "S", "800 chars", "Fixed character window length"],
        ["Overlap Length", "O", "120 chars", "Sliding overlap to preserve context"],
        ["Embedding Dim", "D", "384", "Output dimension of all-MiniLM-L6-v2"],
        ["Top-K Candidates", "K", "4 chunks", "Maximum retrieved context segments"],
        ["Minimum Cutoff", "theta", "0.35", "Cosine threshold for candidate retrieval"],
        ["Confidence Floor", "tau", "0.60", "Threshold below which tickets are suggested"]
    ]
)

add_heading_2("C. Human-in-the-Loop Ticket Resolution Pipeline")
add_body("When an automated query is deemed inconclusive or requires physical administrative authorization (e.g., equipment procurement, leave sanction), the request transitions into the ticketing engine. The system generates an immutable identifier conforming to TKT-YYYY-XXXXXXXX (where Y is the current calendar year and X is a pseudorandom alphanumeric token). The lifecycle follows a strict finite state machine: S in {Open, InProgress, Resolved, Closed}. Administrative permissions allow any designated Department Officer, Department Admin, or Super Administrator to review submitted tickets, post official resolution guidance, append chronological status updates, and archive completed cases.")

# SECTION VI
add_heading_1("VI. Results and Discussion")
add_heading_2("A. Experimental Environment")
add_body("Experimental evaluation was conducted across two discrete execution profiles: (1) Local On-Premise Environment: Windows 11 OS, AMD Ryzen / Intel Core i7 architecture, 16 GB DDR4 RAM, Ollama runtime running quantized llama3.2 (3-billion parameter model), and local SQLite/PostgreSQL; and (2) Production Cloud Infrastructure: Global edge deployment utilizing Vercel CDN for the React SPA, Render Linux Container (Python 3.11 runtime) for the REST API gateway, and AWS Singapore (ap-southeast-1) managed PostgreSQL via Supabase connection pooling.")

add_table(
    "Table IV: Quantitative System Performance and Latency Metrics",
    ["Performance Parameter", "Target SLA", "Measured Local", "Measured Cloud", "Evaluation Criterion"],
    [
        ["Chat Response Latency (LLM Active)", "< 10.0 s", "5.0 - 8.0 s", "Model Offloaded", "Full RAG pipeline inference"],
        ["Fallback Search Latency (Lexical Mode)", "< 2.0 s", "0.4 - 0.8 s", "0.4 - 1.2 s", "Lightweight vector-to-text fallback"],
        ["Document Indexing Latency (500 words)", "< 30.0 s", "14.2 s", "15.0 s", "Ingestion, chunking, and ChromaDB insert"],
        ["Ticket Listing Query (100 records)", "< 2.0 s", "0.8 s", "1.0 s", "REST API query execution and UI render"],
        ["Dashboard Analytics Aggregation", "< 3.0 s", "1.2 s", "1.5 s", "Complex SQL join and metric aggregation"],
        ["Concurrent Stress Capacity", "100 users", "100 users", "100 users", "Simulated parallel clients without failure"]
    ]
)

add_heading_2("B. Retrieval Precision and RAG Effectiveness")
add_body("The system was pre-seeded with 15 verified regulatory circulars across 5 departments (HR, Finance, IT, Pension, Administration). The retrieval engine was evaluated against 50 representative benchmark queries covering leave rules, travel allowances, digital life certificates, and workstation allocations.")

add_table(
    "Table V: RAG Knowledge Retrieval & Grounding Evaluation",
    ["Metric Parameter", "Measured Value", "Evaluation Protocol"],
    [
        ["Configured Departments", "5", "Administrative operational units"],
        ["Indexed Policy Documents", "15 circulars", "3 comprehensive official guidelines/department"],
        ["Mean Cosine Confidence Score", "0.78", "Evaluated on valid domain inquiries"],
        ["Positive User Feedback Rate", "85.0%", "Binary telemetry via thumbs-up/down feedback"],
        ["Test-Set Hallucination Rate", "0.0%", "Zero ungrounded responses when threshold applied"],
        ["Fallback Engagement Rate", "100.0%", "Unindexed queries correctly escalated to tickets"]
    ]
)

add_table(
    "Table VI: Sample Test Queries, Grounding Sources, and Verification",
    ["Department", "Submitted Test Query", "Grounding Document Cited", "Cosine Score", "Verification Result"],
    [
        ["HR", "What is the annual earned leave entitlement?", "HR_Leave_Rules_2024.pdf", "0.84", "Factual leave days correctly cited"],
        ["Finance", "How do I submit Form 12BB for tax savings?", "Finance_Tax_Declaration_Guide.pdf", "0.81", "Chronological workflow outlined"],
        ["IT", "How do I reset my official NIC email password?", "IT_Email_Security_SOP.pdf", "0.88", "Self-service URL and policy quoted"],
        ["Pension", "What is the eligibility for Family Pension?", "Pension_Scheme_Guidelines.pdf", "0.79", "Dependent thresholds verified"],
        ["Admin", "What are the standard office working hours?", "Admin_Office_Regulations.pdf", "0.92", "Core timings and lunch break cited"],
        ["Cross/Out", "Book flight tickets for personal leisure travel.", "None (Suppressed)", "< 0.35", "Declined; ticket creation suggested"]
    ]
)

add_heading_2("C. System Verification and Acceptance Testing")
add_body("Automated testing protocols confirmed system integrity: (1) Backend Suite: 19 automated pytest cases executed with 100% pass rate (test_auth.py, test_chat.py, test_rag.py, test_tickets.py); (2) Frontend Suite: 5 Vitest component test suites validating auth context guards, token storage, and error boundaries; (3) End-to-End Suite: The automated smoke_test.py pipeline executed sequential operational verification covering /health, /auth/login, /departments/, /chat/ask, and /tickets/ POST endpoints with zero operational failures; and (4) Comprehensive Audit: 33/33 discrete acceptance test criteria were satisfied across authentication, ticket lifecycle, administrative oversight, and mobile client access.")

# SECTION VII
add_heading_1("VII. Limitations")
add_body("While the architecture provides robust enterprise automation, several operational limitations are acknowledged: (1) Linguistic Coverage: The prototype currently operates on monolingual English corpora. In multi-lingual administrative settings across India, integration of Hindi and regional languages is necessary; (2) Local Compute Constraints: High-throughput on-premise execution of quantized LLMs requires localized workstation GPUs. On CPU-only nodes, inference latencies can extend during peak loads; and (3) Lack of Real-Time ERP Binding: The system functions over static document indexes and does not execute transactional mutations within legacy government HRMS or integrated financial management systems.")

# SECTION VIII
add_heading_1("VIII. Conclusion and Future Work")
add_body("This paper presented an AI-based multi-department helpdesk portal engineered for public sector governance. By synthesizing dense vector retrieval with on-premise generative models and an automated ticketing lifecycle, the system delivers verifiable, document-grounded responses while establishing a human escalation bridge for administrative resolution. The implementation of strict four-tier RBAC, cryptographic token verification, and automated audit logging guarantees compliance with data privacy mandates.")
add_body("Future research will focus on extending semantic indexing to support Hindi and 22 scheduled Indian languages via multilingual embedding models (e.g., IndicBERT), implementing voice-driven natural language interfaces for accessibility, incorporating Optical Character Recognition (OCR) pipelines to parse scanned archival circulars, and developing federated API connectors for secure integration with state e-governance platforms such as DigiLocker, UMANG, and HRMS.")

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
print("SUCCESS: Exact format IEEE DOCX generated.")
