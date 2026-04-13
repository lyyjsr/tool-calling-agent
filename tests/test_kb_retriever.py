from app.kb.retriever import KBRetriever, tokenize_text


def test_tokenize_text_handles_chinese_and_english() -> None:
    tokens = tokenize_text("API 发布检查清单")

    assert len(tokens) > 0
    assert "api" in tokens
    assert "发" in tokens
    assert "布" in tokens


def test_retriever_finds_code_review_doc() -> None:
    retriever = KBRetriever.from_default_documents()
    results = retriever.search("代码评审流程是什么", top_k=3)

    assert len(results) > 0
    assert results[0].source == "code_review.md"


def test_retriever_finds_incident_doc() -> None:
    retriever = KBRetriever.from_default_documents()
    results = retriever.search("严重故障怎么处理", top_k=3)

    assert len(results) > 0
    assert results[0].source == "incident_response.md"