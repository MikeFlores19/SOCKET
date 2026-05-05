import socket
import os

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("0.0.0.0", 5000))
servidor.listen()

print("Servidor activo...")

while True:
    conn, addr = servidor.accept()
    print(f"Conexión desde {addr}")

    # Recibir nombre del archivo
    nombre_archivo = conn.recv(1024).decode()
    print(f"Solicitan: {nombre_archivo}")

    if os.path.exists(nombre_archivo):
        conn.send("EXITO".encode())

        with open(nombre_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()

        conn.send(contenido.encode())
    else:
        conn.send("ERROR".encode())

    conn.close()