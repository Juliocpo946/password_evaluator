from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Password Evaluator API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    ENTROPY_WEAK_THRESHOLD: float = 60.0
    ENTROPY_STRONG_THRESHOLD: float = 80.0
    
    CHARSET_LOWERCASE: int = 26
    CHARSET_UPPERCASE: int = 26
    CHARSET_DIGITS: int = 10
    CHARSET_SYMBOLS: int = 32
    
    DICTIONARY_PATH: str = "data/passwords.csv"
    DICTIONARY_PENALTY: float = 40.0
    
    ATTACK_RATE: int = 100_000_000_000
    
    class Config:
        case_sensitive = True

settings = Settings()