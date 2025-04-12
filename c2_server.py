import socket
from c2_console import C2Console

HOST = '0.0.0.0'
PORT = 4444

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[+] Listening on {HOST}:{PORT}")

    client_socket, addr = server.accept()
    cli = C2Console(client_socket, addr)
    cli.cmdloop()

    client_socket.close()
    server.close()

if __name__ == "__main__":
    start_server()
