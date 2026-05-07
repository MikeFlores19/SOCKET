import socket
import os
import logging
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8080

# ── CONFIGURACIÓN LOGGING ───────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("ServidorHTTP")

# ── Tipos MIME ──────────────────────────────────────────────
MIME = {
    ".html": "text/html; charset=utf-8",
    ".txt":  "text/plain; charset=utf-8",
    ".css":  "text/css",
    ".js":   "application/javascript",
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
}

# ── Plantilla HTML para archivos .txt ───────────────────────
def txt_en_html(nombre, contenido):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>{nombre}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #0d0d0d;
      color: #e8e8e0;
      font-family: 'Courier New', monospace;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 60px 20px;
    }}
    header {{
      width: 100%;
      max-width: 800px;
      border-bottom: 1px solid #333;
      padding-bottom: 16px;
      margin-bottom: 40px;
    }}
    header span {{
      font-size: 11px;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: #4dffb4;
    }}
    header h1 {{
      font-size: 28px;
      font-weight: normal;
      margin-top: 8px;
      color: #fff;
    }}
    pre {{
      background: #161616;
      border: 1px solid #2a2a2a;
      border-left: 3px solid #4dffb4;
      padding: 32px;
      width: 100%;
      max-width: 800px;
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.8;
      font-size: 15px;
      color: #c8ffd8;
    }}
    footer {{
      margin-top: 40px;
      font-size: 11px;
      color: #444;
      letter-spacing: 2px;
    }}
  </style>
</head>
<body>
  <header>
    <span>servidor http · recurso de texto</span>
    <h1>{nombre}</h1>
  </header>
  <pre>{contenido}</pre>
  <footer>servido el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</footer>
</body>
</html>"""

# ── Página 404 ───────────────────────────────────────────────
def pagina_404(recurso):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>404 – No encontrado</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background: #0d0d0d;
      color: #e8e8e0;
      font-family: 'Courier New', monospace;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }}
    .code {{
      font-size: 96px;
      font-weight: bold;
      color: #ff4d6d;
      line-height: 1;
    }}
    .msg {{ font-size: 18px; color: #888; margin-top: 16px; }}
    .recurso {{
      margin-top: 12px;
      font-size: 13px;
      color: #4dffb4;
      background: #161616;
      padding: 8px 20px;
      border: 1px solid #2a2a2a;
      display: inline-block;
    }}
    a {{
      display: inline-block;
      margin-top: 40px;
      color: #4dffb4;
      text-decoration: none;
      font-size: 12px;
      letter-spacing: 2px;
      border-bottom: 1px solid #4dffb4;
      padding-bottom: 2px;
    }}
  </style>
</head>
<body>
  <div class="code">404</div>
  <p class="msg">Recurso no encontrado</p>
  <div class="recurso">{recurso}</div>
  <a href="/">← volver al inicio</a>
</body>
</html>"""

# ── Construir respuesta HTTP ─────────────────────────────────
def construir_respuesta(status, content_type, cuerpo_bytes):
    cabeceras = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(cuerpo_bytes)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return cabeceras.encode() + cuerpo_bytes

# ── Parsear la primera línea del request ─────────────────────
def parsear_request(raw):
    lineas = raw.split("\r\n")
    if not lineas:
        return None
    partes = lineas[0].split(" ")
    if len(partes) < 2:
        return None
    metodo, ruta = partes[0], partes[1]
    return metodo, ruta

# ── Servidor principal ───────────────────────────────────────
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((HOST, PORT))
servidor.listen(5)

logger.info(f"Servidor HTTP activo → http://localhost:{PORT}")
logger.info(f"Carpeta de recursos : {os.getcwd()}")

while True:

    conn, addr = servidor.accept()
    logger.info(f"Conexión desde {addr[0]}:{addr[1]}")

    try:

        raw = conn.recv(4096).decode(errors="replace")

        if not raw:
            logger.warning("Request vacío")
            conn.close()
            continue

        resultado = parsear_request(raw)

        if not resultado:
            logger.warning("Request inválido")
            conn.close()
            continue

        metodo, ruta = resultado

        if ruta == "/":
            ruta = "/index.html"

        nombre_archivo = ruta.lstrip("/").split("?")[0]
        ext = os.path.splitext(nombre_archivo)[1].lower()

        logger.info(f"{metodo} /{nombre_archivo}")

        if os.path.isfile(nombre_archivo):

            modo = "rb" if ext not in (".html", ".txt", ".css", ".js") else "r"

            if modo == "r":

                with open(nombre_archivo, "r", encoding="utf-8") as f:
                    contenido_str = f.read()

                if ext == ".txt":
                    html = txt_en_html(nombre_archivo, contenido_str)
                    cuerpo = html.encode("utf-8")
                    content_type = "text/html; charset=utf-8"

                else:
                    cuerpo = contenido_str.encode("utf-8")
                    content_type = MIME.get(ext, "text/plain")

            else:

                with open(nombre_archivo, "rb") as f:
                    cuerpo = f.read()

                content_type = MIME.get(ext, "application/octet-stream")

            respuesta = construir_respuesta(
                "200 OK",
                content_type,
                cuerpo
            )

            logger.info(f"200 OK ({len(cuerpo)} bytes)")

        else:

            html404 = pagina_404(nombre_archivo)

            cuerpo = html404.encode("utf-8")

            respuesta = construir_respuesta(
                "404 Not Found",
                "text/html; charset=utf-8",
                cuerpo
            )

            logger.warning(f"404 Not Found → {nombre_archivo}")

        conn.sendall(respuesta)

    except Exception as e:

        logger.error(f"Error interno: {e}")

    finally:

        conn.close()
        logger.info("Conexión cerrada")