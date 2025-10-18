import csv
from typing import Set
from app.core.config import settings
from app.core.logger import setup_logger
from enum import Enum

logger = setup_logger(__name__)

class MatchType(str, Enum):
    NO_MATCH = "NO_MATCH"
    EXACT_MATCH = "EXACT_MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"

class PasswordDictionary:
    _instance = None
    _passwords: Set[str] = set()
    _loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load(self):
        if self._loaded:
            return
        
        try:
            with open(settings.DICTIONARY_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    password = row.get('password', '').strip()
                    if password:
                        self._passwords.add(password.lower())
            self._loaded = True
        except FileNotFoundError:
            logger.error(f"Archivo de diccionario no encontrado: {settings.DICTIONARY_PATH}")
        except Exception as e:
            logger.error(f"Error al cargar diccionario: {str(e)}")
    
    def check_password(self, password: str) -> MatchType:
        if not self._loaded:
            self.load()
        
        password_lower = password.lower()
        
        if password_lower in self._passwords:
            return MatchType.EXACT_MATCH
            
        for dict_pass in self._passwords:
            if dict_pass in password_lower:
                return MatchType.PARTIAL_MATCH
        
        return MatchType.NO_MATCH

dictionary = PasswordDictionary()