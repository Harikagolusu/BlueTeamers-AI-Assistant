from pydantic import Field
from app.tools.domain.schemas.base_schema import BaseSchema

class HashSchema(BaseSchema):
    data: str = Field(..., description="Data to hash")
    algorithm: str = Field("sha256", description="Hashing algorithm (e.g., md5, sha1, sha256)")
