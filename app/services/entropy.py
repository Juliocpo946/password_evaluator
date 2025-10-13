import math
import string
from app.core.config import settings
from app.services.dictionary import dictionary

def calculate_L(password: str) -> int:
    return len(password)

def calculate_N(password: str) -> int:
    keyspace = 0
    
    if any(c in string.ascii_lowercase for c in password):
        keyspace += settings.CHARSET_LOWERCASE
    
    if any(c in string.ascii_uppercase for c in password):
        keyspace += settings.CHARSET_UPPERCASE
    
    if any(c in string.digits for c in password):
        keyspace += settings.CHARSET_DIGITS
    
    if any(c in string.punctuation for c in password):
        keyspace += settings.CHARSET_SYMBOLS
    
    return keyspace

def calculate_entropy(password: str) -> float:
    L = calculate_L(password)
    N = calculate_N(password)
    
    if N == 0:
        return 0.0
    
    return L * math.log2(N)

def check_password_strength(password: str, entropy: float) -> tuple[str, float]:
    effective_entropy = entropy
    
    if dictionary.contains(password):
        effective_entropy = max(0, entropy - settings.DICTIONARY_PENALTY)
    
    if effective_entropy < settings.ENTROPY_WEAK_THRESHOLD:
        strength = "Débil"
    elif effective_entropy < settings.ENTROPY_STRONG_THRESHOLD:
        strength = "Fuerte"
    else:
        strength = "Muy Fuerte"
    
    return strength, effective_entropy

def estimate_crack_time(entropy: float) -> str:
    total_combinations = 2 ** entropy
    seconds = total_combinations / (2 * settings.ATTACK_RATE)
    
    if seconds < 60:
        return f"{seconds:.2f} segundos"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} minutos"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} horas"
    elif seconds < 31536000:
        return f"{seconds / 86400:.2f} días"
    else:
        years = seconds / 31536000
        if years > 1_000_000_000:
            return f"{years:.2e} años"
        return f"{years:.2f} años"