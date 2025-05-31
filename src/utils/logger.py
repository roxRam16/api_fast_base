import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os
from ..database.mongodb import MongoDB
from config import Settings
from dotenv import load_dotenv

load_dotenv()

# ---------- 1) Configuración de MongoDB ----------

class MongoHandler(logging.Handler):

    def emit(self, record: logging.LogRecord):
        log_entry = {
            "timestamp": datetime.utcnow(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module or "undefined",
            "function": record.funcName or "undefined",
            "line": record.lineno
        }
        try:
           collection = MongoDB.get_collection_logs()             
           collection.insert_one(log_entry)
        except Exception as e:
            print(f"[MongoLogger] Error guardando log en MongoDB: {e}")


# Logger central
logger = logging.getLogger("InventorIA")

# El nivel raíz depende de si estamos en dev o prod:
if Settings.APP_ENV:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Formato común
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s (%(funcName)s:%(lineno)d): %(message)s"
)


# 2a) Handler de archivo local (siempre)
file_handler = RotatingFileHandler("inventoria.log", maxBytes=1_000_000, backupCount=3)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
file_handler.stream.reconfigure(encoding='utf-8') 
logger.addHandler(file_handler)

# 2b) Handler de consola: solo en desarrollo
if Settings.APP_ENV:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    # Evitamos errores de codificación en Windows con emojis u otros Unicode
    try:
        console_handler.stream.reconfigure(encoding='utf-8')
    except Exception:
        pass
    logger.addHandler(console_handler)

# 2c) Handler de MongoDB

mongo_handler = MongoHandler()
mongo_handler.setFormatter(formatter)
mongo_handler.setLevel(logging.INFO)
logger.addHandler(mongo_handler)


