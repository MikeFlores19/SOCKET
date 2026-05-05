import socket

HOST = "127.0.0.1"
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

archivo = input("Nombre del archivo: ")
cliente.send(archivo.encode())

respuesta = cliente.recv(4096).decode()

# Separar código y contenido
lineas = respuesta.split("\n", 1)
codigo = lineas[0]

if codigo == "EXITO":
    print("Archivo recibido:\n")
    print(lineas[1])
else:
    print("Error:", lineas[1])

cliente.close()