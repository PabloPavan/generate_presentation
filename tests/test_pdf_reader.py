from pathlib import Path

import fitz
import pytest

from app.pdf_reader import extract_text_from_pdf


def _create_pdf(path: Path, text: str | None = None) -> None:
    doc = fitz.open()
    page = doc.new_page()
    if text:
        page.insert_text((72, 72), text)
    doc.save(path)
    doc.close()


def test_extract_text_from_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    _create_pdf(pdf_path, "Olá mundo")
    output = extract_text_from_pdf(pdf_path)
    assert "Página 1" in output
    assert "Olá mundo" in output


def test_missing_pdf_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf(tmp_path / "missing.pdf")


def test_empty_pdf_raises(tmp_path: Path) -> None:
    pdf_path = tmp_path / "empty.pdf"
    _create_pdf(pdf_path)
    with pytest.raises(ValueError):
        extract_text_from_pdf(pdf_path)
