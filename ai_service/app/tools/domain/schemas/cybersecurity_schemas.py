from pydantic import Field, AnyUrl, IPvAnyAddress, constr
from app.tools.domain.schemas.base_schema import BaseSchema

class ThreatSchema(BaseSchema):
    indicator: str = Field(..., max_length=2048, description="The indicator to look up (IP, domain, hash)")

class IocSchema(BaseSchema):
    ioc: str = Field(..., max_length=2048, description="Indicator of compromise")

class HashReputationSchema(BaseSchema):
    file_hash: str = Field(..., min_length=32, max_length=128, description="MD5, SHA1, or SHA256 hash")

class UrlValidationSchema(BaseSchema):
    url: str = Field(..., max_length=2048, description="URL to validate")

class IpUtilitySchema(BaseSchema):
    ip_address: str = Field(..., max_length=45, description="IP address to analyze")
    action: str = Field(default="geolocation", description="Action: 'geolocation', 'asn', 'reputation'")
