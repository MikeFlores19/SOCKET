from pathlib import Path

from markitdown import MarkItDown

from app.services.ocr_service import apply_ocr


def convert_pdf_to_markdown(
    file_path: str
) -> tuple[str, Path]:
    """
    Convierte un PDF a Markdown.

    Primero aplica OCR y posteriormente
    convierte el documento utilizando
    MarkItDown.

    Returns:
        markdown generado y la ruta
        del PDF procesado con OCR.
    """

    pdf_path = Path(file_path)

    pdf_ocr = apply_ocr(
        pdf_path
    )

    md = MarkItDown()

    result = md.convert(
        str(pdf_ocr)
    )

    markdown = (
        result.text_content
        if hasattr(result, "text_content")
        else str(result)
    )

    return (
        markdown,
        pdf_ocr
    )