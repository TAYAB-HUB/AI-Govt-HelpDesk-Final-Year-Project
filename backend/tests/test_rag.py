from app.services import rag_service


def test_chunk_text_splits_long_text():
    text = "word " * 500
    chunks = rag_service.chunk_text(text, chunk_size=200, overlap=20)
    assert len(chunks) > 1
    for c in chunks:
        assert len(c) <= 200


def test_chunk_text_empty_returns_empty_list():
    assert rag_service.chunk_text("") == []
    assert rag_service.chunk_text("   ") == []


def test_ingest_and_retrieve_roundtrip():
    dept_code = "TESTDEPT"
    text = (
        "Employees are entitled to 30 days of earned leave every year. "
        "Casual leave requests must go through the reporting officer."
    )
    chunk_count = rag_service.ingest_document(dept_code, document_id=9001, document_title="Test Doc", text=text)
    assert chunk_count >= 1

    hits = rag_service.retrieve(dept_code, "How many earned leave days do I get?", top_k=3)
    assert len(hits) >= 1
    assert hits[0]["document_title"] == "Test Doc"
    assert 0.0 <= hits[0]["score"] <= 1.0


def test_retrieve_on_empty_collection_returns_no_hits():
    hits = rag_service.retrieve("EMPTY_DEPT_NO_DOCS", "anything", top_k=3)
    assert hits == []


def test_generate_answer_template_mode_with_no_hits():
    answer, provider = rag_service.generate_answer("random question", [])
    assert provider == "template"
    assert "ticket" in answer.lower()


def test_generate_answer_template_mode_with_hits():
    hits = [{"text": "Leave is 30 days per year.", "document_title": "Leave Policy", "document_id": 1, "score": 0.9}]
    answer, provider = rag_service.generate_answer("How much leave?", hits)
    assert provider == "template"
    assert "Leave Policy" in answer
