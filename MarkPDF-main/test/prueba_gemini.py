from app.services.ai_service import improve_markdown

texto = """
titulo

este es un documento

-uno
-dos
-tres
"""

print(
    improve_markdown(texto)
)
