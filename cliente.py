import socket

IP_SERVIDOR = "127.0.0.1"  # cambia si es otra PC
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((IP_SERVIDOR, PORT))

# Pedir archivo
archivo = input("Nombre del archivo: ")

#  Enviar solicitud
cliente.sendall(archivo.encode())

# Recibir respuesta
respuesta = cliente.recv(4096).decode()

print("\n--- RESPUESTA DEL SERVIDOR ---")
print(respuesta)

cliente.close()