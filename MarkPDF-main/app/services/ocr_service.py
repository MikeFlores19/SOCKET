from pathlib import Path
import subprocess

from app.core.logger import logger


def apply_ocr(pdf_path: Path) -> Path:
    """
    Ejecuta OCR sobre un PDF utilizando OCRmyPDF.

    Args:
        pdf_path: Ruta del PDF original.

    Returns:
        Ruta del PDF procesado con OCR.
    """

    output_pdf = pdf_path.with_stem(
        f"{pdf_path.stem}_ocr"
    )

    logger.info(
        f"Iniciando OCR sobre {pdf_path.name}"
    )

    try:

        subprocess.run(
            [
                "ocrmypdf",

                "--skip-text",

                "--rotate-pages",

                "--deskew",

                "-l",
                "spa+eng",

                str(pdf_path),

                str(output_pdf),
            ],
            check=True,
            capture_output=True,
            text=True
        )

        logger.info(
            f"OCR completado correctamente: {output_pdf.name}"
        )

        return output_pdf

    except subprocess.CalledProcessError as error:

        logger.error(
            f"OCR falló: {error.stderr}"
        )

        raise RuntimeError(
            "No fue posible ejecutar OCR."
        )