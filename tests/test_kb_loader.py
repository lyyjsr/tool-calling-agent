from app.kb.loader import load_kb_documents

def test_load_kb_documents() -> None:
    documents = load_kb_documents()

    assert len(documents) >= 6

    sources = {doc.source for doc in documents}
    assert "onboarding.md" in sources
    assert "code_review.md" in sources
    assert "incident_response.md" in sources
    assert "api_release.md" in sources
    assert "bug_triage.md" in sources
    assert "task_workflow.md" in sources

    for doc in documents:
        assert doc.title.strip() != ""
        assert doc.content.strip() != ""