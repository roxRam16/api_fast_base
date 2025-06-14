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


#Documentación - códigos de status - apis

# Código	Nombre	¿Cuándo usarlo?
# 200	OK	✅ Petición exitosa. Por ejemplo, login exitoso o recurso obtenido.
# 201	Created	✅ Cuando se crea un nuevo recurso. Ej: registro de usuario exitoso.
# 204	No Content	✅ Acción exitosa, pero sin contenido que retornar. Ej: borrado exitoso.
# 400	Bad Request	❌ La petición es inválida. Ej: no se envió la contraseña, faltan campos.
# 401	Unauthorized	❌ No autenticado. Ej: token JWT ausente o inválido.
# 403	Forbidden	❌ Autenticado, pero sin permisos. Ej: usuario sin rol suficiente.
# 404	Not Found	❌ El recurso no existe. Ej: email no registrado.
# 409	Conflict	❌ Conflicto con estado actual. Ej: email ya registrado.
# 422	Unprocessable Entity	❌ Datos bien formateados pero inválidos. Ej: email mal formado. (FastAPI lo usa por defecto para validaciones con Pydantic)
# 500	Internal Server Error	❌ Error inesperado en el servidor. Ej: falla al conectar con MongoDB.


# Resumen
# Situación	Código sugerido
# Falta un campo requerido	400
# Formato inválido de un campo	422
# Email ya existe en la base	409 ✅
# Login sin token	401
# Usuario sin permiso	403