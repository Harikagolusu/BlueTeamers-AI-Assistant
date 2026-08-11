import json
import os
from app.security.interfaces.i_secrets import ISecretProvider
from app.security.secrets.encryption import EncryptionService

class LocalSecretProvider(ISecretProvider):
    def __init__(self, file_path: str, encryption: EncryptionService):
        self._file_path = file_path
        self._encryption = encryption

    def _read_data(self):
        if not os.path.exists(self._file_path):
            return {}
        with open(self._file_path, "r") as f:
            return json.load(f)

    def _write_data(self, data):
        with open(self._file_path, "w") as f:
            json.dump(data, f)

    def get_secret(self, secret_id: str) -> str:
        data = self._read_data()
        if secret_id not in data:
            raise KeyError(f"Secret {secret_id} not found.")
        encrypted = data[secret_id]
        return self._encryption.decrypt(encrypted)

    def set_secret(self, secret_id: str, value: str) -> None:
        data = self._read_data()
        data[secret_id] = self._encryption.encrypt(value)
        self._write_data(data)

# Stubs for Cloud Providers
class AWSSecretProvider(ISecretProvider):
    def get_secret(self, secret_id: str) -> str: pass
    def set_secret(self, secret_id: str, value: str) -> None: pass
