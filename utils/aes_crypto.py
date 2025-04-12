from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import os

# Chave de 32 bytes (AES-256) - pode ser trocada depois
KEY = b'MinhaChaveTopSeguraDe32Bytes!!1234'  # Exatamente 32 bytes

def encrypt(data: str) -> bytes:
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(iv + ct)

def decrypt(encrypted_data: bytes) -> str:
    raw = base64.b64decode(encrypted_data)
    iv = raw[:16]
    ct = raw[16:]

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ct) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode()
