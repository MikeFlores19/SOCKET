import socket
import os  # para verificar archivos

HOST = "0.0.0.0"
PORT = 5000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

print("Servidor activo en puerto 5000...")

while True:
    conn, addr = servidor.accept()
    print(f"Conexión desde {addr}")

    try:
        # Recibir nombre del archivo
        nombre_archivo = conn.recv(1024).decode().strip()
        print(f"Cliente solicitó: {nombre_archivo}")

        # Verificar si existe
        if os.path.exists(nombre_archivo):

            with open(nombre_archivo, "r", encoding="utf-8") as f:
                contenido = f.read()

            respuesta = "EXITO\n" + contenido

        else:
            respuesta = "ERROR: Archivo no encontrado"

        # Enviar respuesta
        conn.sendall(respuesta.encode())

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()
        print("Conexión cerrada\n")