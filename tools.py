"""Tools used by agents.

Fixes included:
- Removed invalid imports and undefined classes (Pdf)
- Implemented a real PDF reader using pypdf
- Exposed a CrewAI tool callable (read_financial_document)

Notes:
- The search tool (Serper) is optional; this assignment can work without external search.
"""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv

from crewai_tools import tool

load_dotenv()


@tool("read_financial_document")
def read_financial_document(path: str = "data/sample.pdf", max_chars: int = 180_000) -> str:
    """Read a PDF from disk and return extracted text.

    Args:
        path: Path to the PDF.
        max_chars: Hard cap to prevent sending extremely large docs to the LLM.

    Returns:
        Extracted text.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if no text could be extracted.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF not found at path: {path}")

    from pypdf import PdfReader

    reader = PdfReader(path)
    pages_text = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        txt = "\n".join(line.rstrip() for line in txt.splitlines() if line.strip() != "")
        if txt:
            pages_text.append(txt)

    full_text = "\n\n".join(pages_text).strip()
    if not full_text:
        raise ValueError(
            "No text could be extracted from the PDF. The file might be scanned images; add OCR if needed."
        )

    return full_text[:max_chars]


# Optional: keep a search tool wired if SERPER_API_KEY is present.
try:
    from crewai_tools.tools.serper_dev_tool import SerperDevTool

    search_tool: Optional[SerperDevTool]
    search_tool = SerperDevTool() if os.getenv("SERPER_API_KEY") else None
except Exception:
    search_tool = None
