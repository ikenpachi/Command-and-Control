from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization

def generate_private_key():
    return x25519.X25519PrivateKey.generate()

def get_public_bytes(private_key):
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

def load_peer_public_bytes(peer_bytes):
    return x25519.X25519PublicKey.from_public_bytes(peer_bytes)

def generate_shared_key(private_key, peer_public_key):
    return private_key.exchange(peer_public_key)
