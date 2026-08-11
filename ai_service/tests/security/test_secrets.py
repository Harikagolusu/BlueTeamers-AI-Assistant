import pytest
import os
from app.security.secrets.encryption import EncryptionService
from app.security.secrets.providers import LocalSecretProvider
from app.security.secrets.cache import SecretCache
from app.security.secrets.vault import SecretVault
from app.security.secrets.rotation import SecretRotationManager

def test_secrets_encryption():
    encryption = EncryptionService()
    secret = "my-super-secret"
    cipher = encryption.encrypt(secret)
    assert cipher != secret
    assert encryption.decrypt(cipher) == secret

def test_secrets_vault_and_rotation(tmp_path):
    f_path = str(tmp_path / "secrets.json")
    encryption = EncryptionService()
    provider = LocalSecretProvider(f_path, encryption)
    cache = SecretCache(ttl_minutes=1)
    vault = SecretVault(provider, cache)
    rotation = SecretRotationManager(vault, cache)
    
    vault.store("api-key", "12345")
    
    assert vault.retrieve("api-key") == "12345"
    assert cache.get("api-key") == "12345"
    
    # Rotation invalidates cache
    rotation.rotate_secret("api-key")
    assert cache.get("api-key") is None
