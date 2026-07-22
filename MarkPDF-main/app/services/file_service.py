from pathlib import Path
import shutil
import uuid

from fastapi import UploadFile

from app.core.logger import logger


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_uploaded_pdf(file: UploadFile) -> Path:
    """
    Guarda un PDF recibido.

    Args:
        file: Archivo recibido desde FastAPI.

    Returns:
        Ruta del PDF almacenado.
    """

    pdf_name = f"{uuid.uuid4()}.pdf"

    file_path = UPLOAD_DIR / pdf_name

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.info(
        f"PDF guardado temporalmente: {pdf_name}"
    )

    return file_path


def save_markdown(markdown: str) -> Path:
    """
    Guarda un archivo Markdown temporal.

    Args:
        markdown: Contenido Markdown.

    Returns:
        Ruta del archivo generado.
    """

    md_name = f"{uuid.uuid4()}.md"

    md_path = UPLOAD_DIR / md_name

    with md_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        file.write(markdown)

    logger.info(
        f"Markdown temporal creado: {md_name}"
    )

    return md_path


def delete_file(file_path: Path) -> None:
    """
    Elimina un archivo temporal si existe.

    Args:
        file_path: Ruta del archivo.
    """

    try:

        if file_path.exists():

            file_path.unlink()

            logger.info(
                f"Archivo eliminado: {file_path.name}"
            )

    except Exception as error:

        logger.warning(
            f"No fue posible eliminar {file_path.name}: {error}"
        )


def delete_files(*files: Path) -> None:
    """
    Elimina múltiples archivos temporales.

    Args:
        *files: Rutas de archivos.
    """

    for file in files:

        delete_file(file)
