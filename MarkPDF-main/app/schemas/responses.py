from pydantic import BaseModel


class HealthResponse(BaseModel):
    message: str


class ConvertResponse(BaseModel):
    filename: str
    markdown: str
