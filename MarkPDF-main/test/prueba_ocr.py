from pathlib import Path

from app.services.ocr_service import apply_ocr

# Cambia el nombre por alguno de los PDFs que tengas en uploads
pdf = Path("uploads/carta_aceptacion.pdf")

resultado = apply_ocr(pdf)

print("PDF original :", pdf)
print("PDF OCR      :", resultado)
