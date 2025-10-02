import os
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def derive_key(password: str, salt: bytes = b"1234567890abcdef") -> bytes:
    return pbkdf2_hmac("sha256", password.encode(), salt, 200000, dklen=32)

def encrypt(key: bytes, plaintext: str) -> bytes:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return nonce + ciphertext  # store nonce + ciphertext together

def decrypt(key: bytes, token: bytes) -> str:
    aesgcm = AESGCM(key)
    nonce = token[:12]
    ciphertext = token[12:]
    return aesgcm.decrypt(nonce, ciphertext, None).decode()
