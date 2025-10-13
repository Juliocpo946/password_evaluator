import logging
import sys
from datetime import datetime

class CustomFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        module = record.name.upper()
        level = record.levelname
        message = record.getMessage()
        return f"[{timestamp}] [{module}] [{level}] {message}"

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CustomFormatter())
    
    logger.addHandler(handler)
    return logger