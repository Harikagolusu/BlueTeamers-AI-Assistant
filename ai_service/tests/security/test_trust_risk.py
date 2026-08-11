import pytest
from app.security.trust.signatures import SignatureValidator
from app.security.trust.certificates import CertificateValidator
from app.security.trust.validator import TrustValidator
from app.security.risk.analyzers import TrustAnalyzer, PermissionAnalyzer
from app.security.risk.aggregator import RiskAggregator
from app.security.risk.pipeline import RiskPipeline

class MockPackage:
    def __init__(self, sig, perms):
        self.signature = sig
        self.permissions = perms
        self.certificate_id = "cert123"

def test_trust_validator():
    validator = TrustValidator(SignatureValidator(), CertificateValidator())
    
    # Valid package
    pkg = MockPackage("valid_sig", [])
    assert validator.validate_trust(pkg) == True
    
def test_risk_pipeline():
    analyzers = [TrustAnalyzer(), PermissionAnalyzer()]
    aggregator = RiskAggregator()
    pipeline = RiskPipeline(analyzers, aggregator)
    
    # High risk package (no signature, destructive perms)
    bad_pkg = MockPackage(None, ["fs.write", "net.connect", "exec"])
    risk = pipeline.evaluate(bad_pkg)
    assert risk in ["HIGH", "CRITICAL"]
    
    # Low risk package (signature, no perms)
    good_pkg = MockPackage("valid_sig", [])
    risk = pipeline.evaluate(good_pkg)
    assert risk == "LOW"
