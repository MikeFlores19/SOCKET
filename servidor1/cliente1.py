import socket

IP_SERVIDOR = "127.0.0.1"

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((IP_SERVIDOR, 5000))

archivo = input("Archivo a solicitar: ")
cliente.send(archivo.encode())

respuesta = cliente.recv(1024).decode()

if respuesta == "EXITO":
    print("Archivo recibido:\n")
    contenido = cliente.recv(4096).decode()
    print(contenido)
else:
    print("Error: archivo no encontrado")

cliente.close()