from fastapi import FastAPI

from app.routers.pdf import router

app = FastAPI(
    title="MarkPDF API",
    description="API para conversión de PDF a Markdown",
    version="0.1.0"
)

app.include_router(router)

