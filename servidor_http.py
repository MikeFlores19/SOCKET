import socket
import os

CARPETA="./files"
PUERTO=5000

# Multipurpose Internet Mail Extensions (identificar que tipo de archivo en la web)
TIPOS_MIME={
    ".html":"text/html;charset=utf-8",
    ".txt":"text/plain;charset=utf-8",
    ".json": "application/json; charset=utf-8",
}

def obtener_mime(ruta):
    _, ext=os.path.splitext(ruta)
    return TIPOS_MIME.get(ext.lower(),"application/octet-stream") #si no encuentra la extension para que no mande error manda "application/octet-stream"


#Respuesta http
def construir_respuesta(codigo,mensaje,content_type,cuerpo):
    cabecera=(
        f"HTTP/1.1 {codigo} {mensaje}\r\n" #version de protocolo
        f"Content-Type: {content_type}\r\n" #tipo  de archivo que va en el cuerpo (MIME)
        f"Content-Length: {len(cuerpo)}\r\n" #cuantos bytes mide el cuerpo
        f"Connection:close\r\n" #cerrar la conexion cuando se termina de enviar algo
        f"\r\n"
    )
    return cabecera.encode("utf-8") + cuerpo #el cuerpo ya es bytes por eso no se codifica

servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # Permite reutilizar el puerto al reiniciar el servidor
servidor.bind(("0.0.0.0", PUERTO))
servidor.listen()
print(f"Servidor escuchando en http://localhost:{PUERTO}")

while True:
    conn,addr=servidor.accept()
    peticion= conn.recv(4096).decode("utf-8",errors="ignore")
    # 'peticion' contiene la petición HTTP completa que mandó el navegador.
    # Ejemplo de su contenido:
    #   GET /index.html HTTP/1.1\r\n
    #   Host: localhost:5000\r\n
    #   User-Agent: Mozilla/5.0...\r\n
    #   Accept: text/html...\r\n
    #   Connection: keep-alive\r\n
    #   \r\n

    if not peticion:
        conn.close()
        continue

    
    primera_linea=peticion.split("\r\n")[0] #GET /index.html HTTP/1.1
    partes=primera_linea.split(" ") # GET, /index.html, HTTP/1.1
    metodo=partes[0] #GET
    recurso=partes[1] if len(partes)>1 else "/" #/index.html

    print(f">>> {metodo} {recurso}")

    if recurso=="/":
        recurso="/index.html"
    ruta=os.path.join(CARPETA,recurso.lstrip("/"))

    if os.path.isfile(ruta): #si existe la ruta
        with open(ruta,"rb") as f: #lee en bytes
            cuerpo=f.read() # lee todo el contenido  dle archivo
        respuesta=construir_respuesta(200,"OK",obtener_mime(ruta),cuerpo) #obtener_mime apra que el navegador sepa como interpretar el contenido
    else:
        cuerpo=b"<h1>404 - NO ENCONTRADO <h1>"
        respuesta = construir_respuesta(404, "Not Found", "text/html; charset=utf-8", cuerpo)

    conn.sendall(respuesta)
    conn.close()