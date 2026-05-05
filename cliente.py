import socket
import threading

IP_SERVIDOR = "127.0.0.1" # Cambia por la IP real del servidor
nombre = input("Tu nombre: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((IP_SERVIDOR, 5000))
cliente.send(nombre.encode())

def recibir():
    while True:
        try:
            msg = cliente.recv(1024).decode()
            print(msg)
        except:
            break

threading.Thread(target=recibir, daemon=True).start()

while True:
    msg = input()
    cliente.send(msg.encode())