# ==========================
# Imagen base
# ==========================
FROM python:3.12-slim

# ==========================
# Variables de entorno
# ==========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ==========================
# Directorio de trabajo
# ==========================
WORKDIR /app

# ==========================
# Dependencias del sistema
# ==========================
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    tesseract-ocr-eng \
    ghostscript \
    ocrmypdf \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# ==========================
# Instalar dependencias Python
# ==========================
COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# ==========================
# Copiar el proyecto
# ==========================
COPY . .

# ==========================
# Crear carpetas necesarias
# ==========================
RUN mkdir -p uploads logs

# ==========================
# Puerto
# ==========================
EXPOSE 8000

# ==========================
# Ejecutar la API
# ==========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]