import socket
import os

CARPETA = "./files"

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("0.0.0.0", 5000))
servidor.listen()
print("Servidor esperando peticiones...")

while True:
    conn, addr = servidor.accept()
    print(f">>> Conexión abierta desde {addr}")

    archivo = conn.recv(1024).decode().strip()
    ruta = os.path.join(CARPETA, archivo)

    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            contenido = f.read()
        respuesta = f"EXITO\n{contenido}"
    else:
        respuesta = "ERROR\nArchivo no encontrado"

    conn.send(respuesta.encode())
    conn.close()
    print(f"<<< Conexión cerrada — archivo: '{archivo}'")