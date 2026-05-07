import socket

IP_SERVIDOR = "127.0.0.1"

archivo = input("Que archivo quieres? (ej: datos.txt): ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((IP_SERVIDOR, 5000))

cliente.send(archivo.encode())

respuesta = cliente.recv(4096).decode()
cliente.close()

lineas = respuesta.split("\n", 1)
codigo = lineas[0]
data = lineas[1] if len(lineas) > 1 else ""

print(f"Codigo: {codigo}")
print(f"Contenido:\n{data}")