from fastapi import APIRouter, HTTPException
from app.models.password import PasswordRequest, PasswordEvaluation
from app.services.entropy import (
    calculate_L,
    calculate_N,
    calculate_entropy,
    check_password_strength,
    estimate_crack_time
)
from app.services.dictionary import dictionary
from app.core.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

dictionary.load()

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
        strength, effective_entropy = check_password_strength(password, entropy)
        is_in_dictionary = dictionary.contains(password)
        crack_time = estimate_crack_time(effective_entropy)
        
        return PasswordEvaluation(
            password_length=L,
            keyspace_size=N,
            entropy_bits=round(entropy, 2),
            effective_entropy_bits=round(effective_entropy, 2),
            strength=strength,
            is_in_dictionary=is_in_dictionary,
            estimated_crack_time=crack_time
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fallo inesperado en evaluación: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno en la evaluación"
        )