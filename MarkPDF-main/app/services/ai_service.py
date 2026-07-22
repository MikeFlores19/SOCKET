from google import genai

from app.core.config import GEMINI_API_KEY
from app.core.logger import logger


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def improve_markdown(markdown: str) -> str:
    """
    Mejora la estructura Markdown utilizando Gemini.

    Si Gemini falla, se devuelve el Markdown original.
    """

    prompt = f"""
Eres un experto en documentos Markdown.

Tu tarea consiste únicamente en mejorar el formato.

Reglas:

- No inventes información.
- No resumas.
- No elimines contenido.
- Corrige títulos.
- Corrige subtítulos.
- Corrige listas.
- Corrige tablas cuando sea posible.
- Mantén todo el texto original.
- De ser necesario realiza una reorganización semántica donde solo puedes reagrupar los fragmentos de texto que pertenezcan lógicamente a la misma idea, flujo conceptual o columna original, separándolos en párrafos distintos, listas o bloques coherentes.  
- Devuelve únicamente Markdown válido.

Documento:

{markdown}
"""

    try:

        logger.info("Enviando Markdown a Gemini...")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        logger.info("Gemini procesó correctamente el documento.")

        return response.text

    except Exception as error:

        logger.error(f"Error utilizando Gemini: {error}")

        logger.info(
            "Se devolverá el Markdown generado por MarkItDown."
        )

        return markdown
