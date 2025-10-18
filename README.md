# API de Evaluación de Contraseñas

## Información General

- **Base URL**: `http://localhost:8000`
- **Versión**: 1.0.0
- **Formato**: JSON

---

## Endpoint: Evaluar Contraseña

### Request

**Method**: `POST`  
**URL**: `/api/v1/password/evaluate`  
**Content-Type**: `application/json`

#### Body Parameters

| Campo | Tipo | Requerido | Restricciones | Descripción |
|-------|------|-----------|---------------|-------------|
| password | string | Sí | 1-128 caracteres | Contraseña a evaluar |

#### Ejemplo de Request

```bash
curl -X POST "http://localhost:8000/api/v1/password/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"password": "MiContraseña123!"}'
```

```json
{
  "password": "MiContraseña123!"
}
```

---

### Response

#### Campos de Respuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| password_length | integer | Longitud de la contraseña (L) |
| keyspace_size | integer | Tamaño del espacio de claves (N) |
| entropy_bits | float | Entropía teórica calculada: L × log₂(N) |
| effective_entropy_bits | float | Entropía real después de penalizaciones |
| strength | string | Clasificación: "Muy Débil", "Débil", "Moderada", "Fuerte", "Muy Fuerte" |
| is_exact_dictionary_match | boolean | Si es idéntica a una palabra del diccionario |
| is_partial_dictionary_match | boolean | Si contiene una palabra del diccionario |
| has_common_patterns | boolean | Si contiene patrones predecibles |
| estimated_crack_time | string | Tiempo estimado de crackeo (10¹² intentos/seg) |
| security_recommendations | array[string] | Lista de mejoras sugeridas |

#### Ejemplo de Response (200 OK)

```json
{
  "password_length": 16,
  "keyspace_size": 94,
  "entropy_bits": 105.23,
  "effective_entropy_bits": 105.23,
  "strength": "Muy Fuerte",
  "is_exact_dictionary_match": false,
  "is_partial_dictionary_match": false,
  "has_common_patterns": false,
  "estimated_crack_time": "5.12e+20 años",
  "security_recommendations": [
    "Contraseña cumple con estándares de seguridad"
  ]
}
```

---

## Códigos de Estado HTTP

### 200 - OK
Evaluación exitosa.

**Ejemplo**:
```json
{
  "password_length": 14,
  "keyspace_size": 62,
  "entropy_bits": 83.36,
  "effective_entropy_bits": 83.36,
  "strength": "Fuerte",
  "is_exact_dictionary_match": false,
  "is_partial_dictionary_match": false,
  "has_common_patterns": false,
  "estimated_crack_time": "1966287.65 años",
  "security_recommendations": [
    "Contraseña cumple con estándares de seguridad"
  ]
}
```

### 400 - Bad Request
Contraseña inválida o parámetros incorrectos.

**Ejemplos**:
```json
{
  "detail": "Contraseña no contiene caracteres válidos"
}
```

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 1 character"
    }
  ]
}
```

### 500 - Internal Server Error
Error interno del servidor.

**Ejemplo**:
```json
{
  "detail": "Error interno en la evaluación"
}
```

---

## Algoritmo de Evaluación

### 1. Cálculo de Entropía Base

```
E = L × log₂(N)
```

**Donde**:
- `L`: Longitud de la contraseña
- `N`: Suma de conjuntos de caracteres utilizados

**Conjuntos de caracteres**:
| Tipo | Cantidad |
|------|----------|
| Minúsculas (a-z) | 26 |
| Mayúsculas (A-Z) | 26 |
| Dígitos (0-9) | 10 |
| Símbolos | 32 |

### 2. Verificación de Diccionario

El sistema verifica contra 1 millón de contraseñas comprometidas:

- **Coincidencia exacta**: La contraseña es idéntica a una del diccionario
- **Coincidencia parcial**: La contraseña contiene una palabra del diccionario

### 3. Penalizaciones Aplicadas

| Condición | Penalización |
|-----------|--------------|
| Coincidencia exacta o parcial en diccionario | × 0.5 (50% de entropía) |
| Patrones comunes detectados | × 0.7 (30% adicional) |

**Aplicación**: Las penalizaciones son multiplicativas sobre la entropía efectiva.

### 4. Patrones Detectados

- Secuencias numéricas: `123`, `234`, `345`, `456`, `567`, `678`, `789`
- Secuencias alfabéticas: `abc`, `bcd`, `cde`
- Patrones de teclado: `qwerty`, `asdfg`
- Caracteres repetidos: `aaa`, `111`

### 5. Clasificación de Fortaleza

| Entropía Efectiva | Clasificación |
|-------------------|---------------|
| 0 - 39 bits | Muy Débil |
| 40 - 59 bits | Débil |
| 60 - 79 bits | Moderada |
| 80 - 119 bits | Fuerte |
| 120+ bits | Muy Fuerte |

### 6. Tiempo de Crackeo

```
Tiempo = (2^E_efectiva) / 10¹²
```

**Tasa de ataque**: 1,000,000,000,000 (10¹²) intentos/segundo

---

## Ejemplos de Uso

### Caso 1: Contraseña Muy Débil

**Request**:
```json
{
  "password": "password123"
}
```

**Response**:
```json
{
  "password_length": 11,
  "keyspace_size": 36,
  "entropy_bits": 56.93,
  "effective_entropy_bits": 19.93,
  "strength": "Muy Débil",
  "is_exact_dictionary_match": true,
  "is_partial_dictionary_match": false,
  "has_common_patterns": true,
  "estimated_crack_time": "0.00 segundos",
  "security_recommendations": [
    "Incrementa la longitud a al menos 12 caracteres",
    "La contraseña es idéntica a una palabra de diccionario. Elígela de nuevo.",
    "Elimina patrones secuenciales o caracteres repetidos",
    "Agrega letras mayúsculas",
    "Agrega símbolos especiales"
  ]
}
```

### Caso 2: Contraseña Fuerte

**Request**:
```json
{
  "password": "C@sa*Verde82"
}
```

**Response**:
```json
{
  "password_length": 12,
  "keyspace_size": 94,
  "entropy_bits": 78.98,
  "effective_entropy_bits": 78.98,
  "strength": "Moderada",
  "is_exact_dictionary_match": false,
  "is_partial_dictionary_match": false,
  "has_common_patterns": false,
  "estimated_crack_time": "15234.56 años",
  "security_recommendations": [
    "Contraseña cumple con estándares de seguridad"
  ]
}
```

### Caso 3: Contraseña Muy Fuerte

**Request**:
```json
{
  "password": "X7#mK9$pL2@qR4&nT6"
}
```

**Response**:
```json
{
  "password_length": 18,
  "keyspace_size": 94,
  "entropy_bits": 118.47,
  "effective_entropy_bits": 118.47,
  "strength": "Fuerte",
  "is_exact_dictionary_match": false,
  "is_partial_dictionary_match": false,
  "has_common_patterns": false,
  "estimated_crack_time": "1.42e+24 años",
  "security_recommendations": [
    "Contraseña cumple con estándares de seguridad"
  ]
}
```

### Caso 4: Error - Contraseña Vacía

**Request**:
```json
{
  "password": ""
}
```

**Response** (400):
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 1 character"
    }
  ]
}
```

---

## Pruebas con cURL

### Linux/Mac
```bash
# Contraseña muy débil
curl -X POST "http://localhost:8000/api/v1/password/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"password": "password123"}'

# Contraseña fuerte
curl -X POST "http://localhost:8000/api/v1/password/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"password": "C@sa*Verde82"}'

# Contraseña muy fuerte
curl -X POST "http://localhost:8000/api/v1/password/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"password": "X7#mK9$pL2@qR4&nT6"}'
```

### Windows PowerShell
```powershell
# Contraseña muy débil
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/password/evaluate" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"password": "password123"}'

# Contraseña fuerte
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/password/evaluate" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"password": "C@sa*Verde82"}'
```

### Python
```python
import requests

url = "http://localhost:8000/api/v1/password/evaluate"
headers = {"Content-Type": "application/json"}

# Contraseña muy débil
response = requests.post(url, json={"password": "password123"}, headers=headers)
print(response.json())

# Contraseña fuerte
response = requests.post(url, json={"password": "C@sa*Verde82"}, headers=headers)
print(response.json())

# Contraseña muy fuerte
response = requests.post(url, json={"password": "X7#mK9$pL2@qR4&nT6"}, headers=headers)
print(response.json())
```

### JavaScript (Fetch API)
```javascript
// Contraseña muy débil
fetch('http://localhost:8000/api/v1/password/evaluate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({password: 'password123'})
})
.then(response => response.json())
.then(data => console.log(data));

// Contraseña fuerte
fetch('http://localhost:8000/api/v1/password/evaluate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({password: 'C@sa*Verde82'})
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Seguridad y Privacidad

### Cero Persistencia
- **No se almacenan contraseñas** en ningún formato
- **No se generan logs** de contraseñas evaluadas
- **Procesamiento en memoria** únicamente
- **Sin base de datos** de contraseñas de usuarios

### Logs Críticos
Solo se registran errores del sistema, nunca datos de usuarios:
```
[2025-10-17 10:30:45] [DICTIONARY] [ERROR] Archivo de diccionario no encontrado
[2025-10-17 10:31:12] [PASSWORD] [ERROR] Fallo inesperado en evaluación
```

### CORS
Configurado para aceptar peticiones de cualquier origen en desarrollo.  
**Recomendación**: Restringir orígenes en producción.

---

## Instalación

### Requisitos
- Python 3.11+
- pip

### Pasos
```bash
# Clonar repositorio
git clone https://github.com/Juliocpo946/password_evaluator.git
cd password_evaluator

# Instalar dependencias
pip install -r requirements.txt

# Verificar estructura
# Asegurar que existe: data/passwords.csv

# Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Acceso
- API: http://localhost:8000/api/v1/password/evaluate
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

---

## Limitaciones Conocidas

1. **Diccionario estático**: 1M contraseñas comprometidas
2. **Patrones básicos**: Detección limitada a patrones comunes
3. **Sin análisis contextual**: No evalúa contraseñas en contexto de usuario
4. **Tasa de ataque fija**: Asume 10¹² intentos/segundo constante

---

## Despliegue en Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Juliocpo946/password_evaluator.git)

### Configuración Manual

1. Crear nuevo Web Service en Render
2. Conectar repositorio de GitHub
3. Configuración automática detectada desde `render.yaml`
4. Deploy automático

---

## Repositorio y Documentación

- **GitHub**: https://github.com/Juliocpo946/password_evaluator.git
- **Postman**: https://documenter.getpostman.com/view/48692012/2sB3QNr