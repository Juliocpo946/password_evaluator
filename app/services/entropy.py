import math
import string
import re
from collections import Counter
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
    
    char_freq = Counter(password)
    unique_chars = len(char_freq)
    
    if unique_chars < L * 0.5:
        repetition_penalty = (unique_chars / L) * 0.7
        return L * math.log2(N) * repetition_penalty
    
    return L * math.log2(N)

def detect_patterns(password: str) -> bool:
    patterns = [
        r'^[A-Z][a-z]+\d+$',
        r'^\d+[A-Za-z]+$',
        r'^[A-Za-z]+\d+$',
        r'(123|234|345|456|567|678|789|890)',
        r'(abc|bcd|cde|def|efg|fgh)',
        r'(qwerty|asdfgh|zxcvbn)',
        r'(.)\1{2,}'
    ]
    
    for pattern in patterns:
        if re.search(pattern, password, re.IGNORECASE):
            return True
    
    return False

def check_dictionary_variants(password: str) -> bool:
    if dictionary.contains(password):
        return True
    
    base = re.sub(r'\d+$', '', password)
    if len(base) >= 4 and dictionary.contains(base):
        return True
    
    base_lower = password.lower()
    base_no_numbers = re.sub(r'\d', '', base_lower)
    if len(base_no_numbers) >= 4 and dictionary.contains(base_no_numbers):
        return True
    
    return False

def check_password_strength(password: str, entropy: float) -> tuple[str, float]:
    effective_entropy = entropy
    penalties = []
    
    if check_dictionary_variants(password):
        penalties.append(settings.DICTIONARY_PENALTY)
    
    if detect_patterns(password):
        penalties.append(25.0)
    
    if len(password) < 8:
        penalties.append(15.0)
    
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c in string.digits for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    
    char_variety = sum([has_lower, has_upper, has_digit, has_symbol])
    if char_variety < 3:
        penalties.append(20.0)
    
    total_penalty = sum(penalties)
    effective_entropy = max(0, entropy - total_penalty)
    
    if effective_entropy < settings.ENTROPY_WEAK_THRESHOLD:
        strength = "Débil"
    elif effective_entropy < settings.ENTROPY_STRONG_THRESHOLD:
        strength = "Fuerte"
    else:
        strength = "Muy Fuerte"
    
    return strength, effective_entropy

def estimate_crack_time(entropy: float) -> str:
    total_combinations = 2 ** entropy
    avg_attempts = total_combinations / 2
    seconds = avg_attempts / settings.ATTACK_RATE
    
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