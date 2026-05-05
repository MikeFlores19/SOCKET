import socket
import threading

clientes = []

def manejar_cliente(conn, nombre):
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"[{nombre}]: {msg}")
            # Reenviar a todos los demás
            for c, n in clientes:
                if c != conn:
                    c.send(f"[{nombre}]: {msg}".encode())
        except:
            break
    clientes.remove((conn, nombre))
    conn.close()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("0.0.0.0", 5000))
servidor.listen()
print("Servidor escuchando en puerto 5000...")

while True:
    conn, addr = servidor.accept()
    nombre = conn.recv(1024).decode()
    clientes.append((conn, nombre))
    print(f"{nombre} se conectó desde {addr}")
    threading.Thread(target=manejar_cliente, args=(conn, nombre)).start()
