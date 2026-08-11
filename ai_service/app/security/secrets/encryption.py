from cryptography.fernet import Fernet
import os

class EncryptionService:
    def __init__(self, key: bytes = None):
        if not key:
            # Fallback to env or generate (not for production)
            env_key = os.getenv("ENTERPRISE_SECRET_KEY")
            self._key = env_key.encode() if env_key else Fernet.generate_key()
        else:
            self._key = key
        self._cipher = Fernet(self._key)

    def encrypt(self, data: str) -> str:
        return self._cipher.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self._cipher.decrypt(token.encode()).decode()
