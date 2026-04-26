import os, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

class SovereignHSM:
    def __init__(self, key_path: str = ".narmer_hsm_key"):
        self.key_path = key_path
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                data = f.read()
                self.encryption_key = data[:32]
                self.signing_seed = data[32:64]
        else:
            self.encryption_key = AESGCM.generate_key(bit_length=256)
            signing_key = Ed25519PrivateKey.generate()
            self.signing_seed = signing_key.private_bytes_raw()
            with open(key_path, "wb") as f:
                f.write(self.encryption_key + self.signing_seed)
        self.aes = AESGCM(self.encryption_key)
        self.signing_key = Ed25519PrivateKey.from_private_bytes(self.signing_seed)
        self.public_key = self.signing_key.public_key()

    def encrypt(self, plaintext: str) -> str:
        nonce = os.urandom(12)
        ct = self.aes.encrypt(nonce, plaintext.encode(), None)
        return base64.b64encode(nonce + ct).decode()

    def decrypt(self, ciphertext: str) -> str:
        raw = base64.b64decode(ciphertext)
        nonce, ct = raw[:12], raw[12:]
        return self.aes.decrypt(nonce, ct, None).decode()

    def sign(self, data: str) -> str:
        return base64.b64encode(self.signing_key.sign(data.encode())).decode()

    def verify(self, data: str, signature_b64: str) -> bool:
        try:
            signature = base64.b64decode(signature_b64)
            self.public_key.verify(signature, data.encode())
            return True
        except:
            return False
