from pydantic import BaseModel, Field, field_validator

class PasswordRequest(BaseModel):
    password: str = Field(..., min_length=1, max_length=128, description="Contraseña a evaluar")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v or v.isspace():
            raise ValueError("La contraseña no puede estar vacía o contener solo espacios")
        return v

class PasswordEvaluation(BaseModel):
    password_length: int
    keyspace_size: int
    entropy_bits: float
    effective_entropy_bits: float
    strength: str
    is_in_dictionary: bool
    has_common_patterns: bool
    estimated_crack_time: str
    security_recommendations: list[str]