from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Parâmetros padrão de DH (p, g)
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())

def generate_private_key():
    return parameters.generate_private_key()

def get_public_bytes(private_key):
    public_key = private_key.public_key()
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def load_peer_public_bytes(public_bytes):
    return serialization.load_pem_public_key(public_bytes, backend=default_backend())

def generate_shared_key(private_key, peer_public_key):
    shared_key = private_key.exchange(peer_public_key)
    return shared_key[:32]  # AES-256 key (first 32 bytes)