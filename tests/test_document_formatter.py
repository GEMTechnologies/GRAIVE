import zipfile
from pathlib import Path

from src.formatting import create_document_formatter


def test_document_formatter_creates_all_outputs(tmp_path):
    formatter = create_document_formatter(str(tmp_path))

    content = """
# Sample Report

Welcome to the *formatted* **document** generator demo.

![System Diagram](diagram.png)

| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |

"""

    result = formatter.format_document(
        content=content.strip(),
        title="Sample Report",
        author="Test Harness",
        output_format="md",
    )

    exports = result.get("exports", {})

    markdown_path = Path(exports.get("md"))
    docx_path = Path(exports.get("docx"))
    pdf_path = Path(exports.get("pdf"))

    assert markdown_path.exists() and markdown_path.suffix == ".md"
    assert docx_path.exists() and docx_path.suffix == ".docx"
    assert pdf_path.exists() and pdf_path.suffix == ".pdf"

    # Docx files are zip archives – ensure they contain document.xml
    with zipfile.ZipFile(docx_path, "r") as docx_zip:
        assert "word/document.xml" in docx_zip.namelist()

    # Generated PDF should be non-empty
    assert pdf_path.stat().st_size > 0

    # Image assets should be materialised
    images_dir = Path(tmp_path) / "images"
    generated_images = list(images_dir.glob("*.png"))
    assert generated_images, "expected at least one generated image"
