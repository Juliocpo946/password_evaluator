import math
import re

def calculate_L(password: str) -> int:
    return len(password)

def calculate_N(password: str) -> int:
    N = 0
    if re.search(r'[a-z]', password):
        N += 26
    if re.search(r'[A-Z]', password):
        N += 26
    if re.search(r'\d', password):
        N += 10
    if re.search(r'[^a-zA-Z\d]', password):
        N += 32
    return N

def calculate_entropy(password: str) -> float:
    L = calculate_L(password)
    N = calculate_N(password)
    if L == 0 or N == 0:
        return 0.0
    return L * math.log2(N)

def check_password_strength(password: str, entropy: float, is_in_dictionary: bool = False) -> tuple[str, float]:
    effective_entropy = entropy
    
    if is_in_dictionary:
        effective_entropy *= 0.5
    
    if detect_patterns(password):
        effective_entropy *= 0.7

    if effective_entropy < 40:
        return "Muy Débil", effective_entropy
    elif effective_entropy < 60:
        return "Débil", effective_entropy
    elif effective_entropy < 80:
        return "Moderada", effective_entropy
    elif effective_entropy < 120:
        return "Fuerte", effective_entropy
    else:
        return "Muy Fuerte", effective_entropy

def estimate_crack_time(entropy: float) -> str:
    crack_speed_hps = 1e12
    seconds_to_crack = (2**entropy) / crack_speed_hps
    
    if seconds_to_crack < 60:
        return f"{seconds_to_crack:.2f} segundos"
    minutes = seconds_to_crack / 60
    if minutes < 60:
        return f"{minutes:.2f} minutos"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.2f} horas"
    days = hours / 24
    if days < 365:
        return f"{days:.2f} días"
    years = days / 365
    if years < 1e6:
        return f"{years:.2f} años"
    elif years < 1e9:
        return f"{years / 1e6:.2f} millones de años"
    else:
        return f"{years / 1e9:.2f} mil millones de años"

def detect_patterns(password: str) -> bool:
    if re.search(r'(.)\1{2,}', password):
        return True
    
    sequences = ['123', '234', '345', '456', '567', '678', '789', 'abc', 'bcd', 'cde', 'qwerty', 'asdfg']
    for seq in sequences:
        if seq in password.lower():
            return True
            
    return False

def check_dictionary_variants(password: str) -> bool:
    from app.services.dictionary import dictionary
    return dictionary.check_password(password) != "NO_MATCH"