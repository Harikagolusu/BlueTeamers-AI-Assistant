from typing import Any
from app.security.interfaces.i_trust import ISignatureValidator

class SignatureValidator(ISignatureValidator):
    def validate_signature(self, package: Any) -> bool:
        # Stub: Verify cryptographic signature of the package
        signature = getattr(package, "signature", None)
        # If enterprise requires signed packages, this would fail if None
        # For stub purposes, allow if signature is present or not strict mode.
        return True
