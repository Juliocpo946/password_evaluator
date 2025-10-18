from pydantic import BaseModel, Field
from typing import List

class PasswordRequest(BaseModel):
    password: str = Field(..., min_length=1)

class PasswordEvaluation(BaseModel):
    password_length: int
    keyspace_size: int
    entropy_bits: float
    effective_entropy_bits: float
    strength: str
    is_exact_dictionary_match: bool
    is_partial_dictionary_match: bool
    has_common_patterns: bool
    estimated_crack_time: str
    security_recommendations: List[str]