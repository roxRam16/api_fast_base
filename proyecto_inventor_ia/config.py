# config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # ----------------------------------------------------
    # 1) MODO DE EJECUCIÓN: "development" o "production"
    # ----------------------------------------------------
    APP_ENV = os.getenv("APP_ENV", "development").lower()

    # ----------------------------------------------------
    # 2) SETTINGS PROJECT
    # ----------------------------------------------------

    PROJECT_NAME = "Invetori API - IDENTITY"

       
    # ----------------------------------------------------
    # 3) CONFIGURACIÓN DE MONGO
    # ----------------------------------------------------
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB = os.getenv("MONGODB_DB", "invetori_db_test")
    MONGODB_COLLECTION_IDENTITY = os.getenv("MONGODB_COLLECTION_IDENTITY", "identity_test")
    MONGODB_COLLECTION_ROLES = os.getenv("MONGODB_COLLECTION_ROLES", "roles_test")
    MONGODB_COLLECTION_PERMISOS = os.getenv("MONGODB_COLLECTION_PERMISOS", "permisos_test")
    MONGODB_COLLECTION_LOGS = os.getenv("MONGODB_COLLECTION_LOGS", "logs_test")

       
    # ----------------------------------------------------
    # 4) JWT
    # ----------------------------------------------------
    JWT_SECRET = os.getenv("JWT_SECRET", "quierosermantenida")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


    # ----------------------------------------------------
    # 3) OTROS Parámetros
    # ----------------------------------------------------
    # · Aquí puedes agregar cualquier otro setting necesario


settings = Settings()
