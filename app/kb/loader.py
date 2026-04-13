from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KBDocument:
    """
    表示一篇知识库文档，定义文档对象
    """
    source: str
    title: str
    content: str


def _get_default_kb_dir() -> Path:
    """
    获取默认知识库目录：
    项目根目录 / data / kb
    """
    project_root = Path(__file__).resolve().parents[2]
    return project_root / "data" / "kb"

def _extract_title(content: str, fallback_filename: str) -> str:
    """
    从 markdown 内容里提取标题。
    如果某一行是 '# 标题'，就用它；
    否则用文件名做兜底标题。
    """
    lines = content.splitlines()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()

    return fallback_filename.replace(".md", "").replace("_", " ").strip().title()


def load_kb_documents(kb_dir: Path | None = None) -> list[KBDocument]:
    """
    加载知识库目录下的所有 markdown 文档。
    返回 KBDocument 列表。
    """
    kb_path = kb_dir or _get_default_kb_dir()

    if not kb_path.exists():
        raise FileNotFoundError(f"Knowledge base directory not found: {kb_path}")

    documents: list[KBDocument] = []

    for file_path in sorted(kb_path.glob("*.md")):
        content = file_path.read_text(encoding="utf-8").strip()

        if not content:
            continue

        title = _extract_title(content, file_path.name)

        documents.append(
            KBDocument(
                source=file_path.name,
                title=title,
                content=content,
            )
        )

    return documents
