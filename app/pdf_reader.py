from __future__ import annotations

from pathlib import Path

import fitz


def extract_text_from_pdf(pdf_path: str | Path, max_chars: int = 80_000) -> str:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    chunks: list[str] = []
    current_len = 0

    with fitz.open(path) as doc:
        for idx, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if not text:
                continue
            chunk = f"--- Página {idx} ---\n{text}\n"
            remaining = max_chars - current_len
            if remaining <= 0:
                break
            if len(chunk) > remaining:
                chunk = chunk[:remaining]
            chunks.append(chunk)
            current_len += len(chunk)
            if current_len >= max_chars:
                break

    output = "\n".join(chunks).strip()
    if not output:
        raise ValueError("No text could be extracted from the PDF.")
    return output
