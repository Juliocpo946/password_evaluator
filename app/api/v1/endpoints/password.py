from fastapi import APIRouter, HTTPException
from app.models.password import PasswordRequest, PasswordEvaluation
from app.services.entropy import (
    calculate_L,
    calculate_N,
    calculate_entropy,
    check_password_strength,
    estimate_crack_time,
    detect_patterns
)
from app.services.dictionary import dictionary, MatchType
from app.core.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

dictionary.load()

def generate_recommendations(
    password: str, 
    strength: str, 
    exact_match: bool, 
    partial_match: bool, 
    has_patterns: bool
) -> list[str]:
    recommendations = []
    
    if len(password) < 12:
        recommendations.append("Incrementa la longitud a al menos 12 caracteres")
    
    if exact_match:
        recommendations.append("La contraseña es idéntica a una palabra de diccionario. Elígela de nuevo.")
    elif partial_match:
        recommendations.append("La contraseña contiene una palabra común de diccionario. Evita usar variaciones predecibles.")
    
    if has_patterns:
        recommendations.append("Elimina patrones secuenciales o caracteres repetidos")
    
    if not any(c.isupper() for c in password):
        recommendations.append("Agrega letras mayúsculas")
    
    if not any(c.islower() for c in password):
        recommendations.append("Agrega letras minúsculas")
    
    if not any(c.isdigit() for c in password):
        recommendations.append("Agrega números")
    
    if not any(not c.isalnum() for c in password):
        recommendations.append("Agrega símbolos especiales")
    
    if strength == "Muy Fuerte" and not recommendations:
        recommendations.append("Contraseña cumple con estándares de seguridad")
    
    return recommendations

@router.post("/evaluate", response_model=PasswordEvaluation)
async def evaluate_password(request: PasswordRequest):
    try:
        password = request.password
        
        L = calculate_L(password)
        N = calculate_N(password)
        
        if N == 0:
            raise HTTPException(
                status_code=400,
                detail="Contraseña no contiene caracteres válidos"
            )
        
        entropy = calculate_entropy(password)
        
        match_result = dictionary.check_password(password)
        is_exact_match = match_result == MatchType.EXACT_MATCH
        is_partial_match = match_result == MatchType.PARTIAL_MATCH
        
        is_in_dictionary_for_strength_check = is_exact_match or is_partial_match
        
        strength, effective_entropy = check_password_strength(password, entropy, is_in_dictionary_for_strength_check)
        has_patterns = detect_patterns(password)
        crack_time = estimate_crack_time(effective_entropy)
        
        recommendations = generate_recommendations(password, strength, is_exact_match, is_partial_match, has_patterns)
        
        return PasswordEvaluation(
            password_length=L,
            keyspace_size=N,
            entropy_bits=round(entropy, 2),
            effective_entropy_bits=round(effective_entropy, 2),
            strength=strength,
            is_exact_dictionary_match=is_exact_match,
            is_partial_dictionary_match=is_partial_match,
            has_common_patterns=has_patterns,
            estimated_crack_time=crack_time,
            security_recommendations=recommendations
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fallo inesperado en evaluación: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno en la evaluación"
        )