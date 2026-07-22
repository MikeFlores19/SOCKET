from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    BackgroundTasks,
)

from fastapi.responses import FileResponse

from app.schemas.responses import (
    HealthResponse,
    ConvertResponse,
)
from app.services.converter import (
    convert_pdf_to_markdown,
)
from app.services.file_service import (
    save_uploaded_pdf,
    save_markdown,
    delete_files,
)
from app.services.ai_service import improve_markdown
from app.core.logger import logger

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Verificar estado de la API"
)
def root() -> HealthResponse:
    """
    Endpoint de verificación de estado.

    Returns:
        Estado actual de la API.
    """

    return HealthResponse(
        message="MarkPDF API funcionando correctamente"
    )

@router.post("/convert", response_model=ConvertResponse)
def convert_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)) -> ConvertResponse:

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten archivos PDF"
        )

    try:

        logger.info(
            f"PDF recibido: {file.filename}"
        )

        file_path = save_uploaded_pdf(file)

        markdown, ocr_pdf = convert_pdf_to_markdown(
            str(file_path)
        )

        markdown = improve_markdown(
            markdown
        )

        background_tasks.add_task(
           delete_files,
           file_path,
           ocr_pdf
        )

        logger.info(
            f"Conversión exitosa: {file.filename}"
        )

        return ConvertResponse(
            filename=file.filename,
            markdown=markdown
        )

    except Exception as error:

        logger.error(
            f"Error procesando {file.filename}: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@router.post("/convert/download")
def convert_pdf_download(background_tasks: BackgroundTasks, file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten archivos PDF"
        )

    try:

        logger.info(
            f"PDF recibido para descarga: {file.filename}"
        )

        file_path = save_uploaded_pdf(file)

        markdown, ocr_pdf = convert_pdf_to_markdown(
            str(file_path)
        )
        
        markdown = improve_markdown(
           markdown
        )
        
        md_path = save_markdown(markdown)


        background_tasks.add_task(
           delete_files,
           file_path,
           ocr_pdf,
           md_path
        )

        with md_path.open("w", encoding="utf-8") as f:
            f.write(markdown)

        logger.info(
            f"Conversión exitosa para descarga: {file.filename}"
        )

        return FileResponse(
            path=md_path,
            filename="documento.md",
            media_type="text/markdown"
        )

    except Exception as error:

        logger.error(
            f"Error procesando {file.filename}: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
