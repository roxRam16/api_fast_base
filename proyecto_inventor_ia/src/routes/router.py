from fastapi import APIRouter
from src.utils.response import ApiResponse
from src.utils.logger import logger
from src.database.mongodb import MongoDB
from config import Settings # nuestro settings.py con la variable APP_ENV

router = APIRouter(prefix="/inventoria/identity")

if Settings.APP_ENV == False:

    entorno = "Production"

else:

    entorno = "Development"


@router.get("/app", tags=["DescripcionAPI"])
async def home():
    logger.info(f"Info:200 - app Home")
    print(f"🚀 app Home")
    return ApiResponse.success(f"🚀 app Home")


# 🟢 Eventos de arranque y apagado
@router.get("/startup", tags=["DescripcionAPI"], summary="Prueba de conexión open")
async def startup_db():
    MongoDB.get_client()
    logger.info(f"Info:200 - Conexión establecida con MongoDB {entorno}")
    print(f"🚀 Conexion establecida con MongoDB {entorno}")
    return ApiResponse.success(f"🚀 Conexión open ok {entorno}")


@router.get("/collection", tags=["DescripcionAPI"], summary="Prueba de conexión collection")
async def collection_db():
    collection = MongoDB.get_collection_identity()
    result = collection.insert_one({"PRUEBA DE INSERCIÓN":"200"})
    if result:
        logger.info(f"Info:200 - COLLECTION IDENTITY OK")
        return ApiResponse.success(f"🚀 COLLECTION ok {entorno}")
    # logger.info(f"Info:200 - COLLECTION IDENTITY OK {entorno}")
    # print(f"🚀 Collection identity {entorno}")
  


# @router.get("/shutdown", tags=["DescripcionAPI"], summary="Prueba de conexión close")
# async def shutdown_db():
#    MongoDB.close_client()
#    logger.info(f"Info:200 - Conexion cerrada con MongoDB {entorno}")
#    print(f"🛑 Conexion cerrada con MongoDB {entorno}")
#    return ApiResponse.success(f"🛑 Conexion cerrada ok {entorno}")


# @router.get("/invetoria/welcome", tags=["DescripcionAPI"], summary="Mensaje de bienvenida")
# async def welcome():
#     return ApiResponse.success(f"😄🐱🚀 Bienvenido a InventorIA {entorno}")


# @router.get("/invetoria/msj_errors", tags=["DescripcionAPI"], summary="Mensaje de error")
# async def bad_request():
#     return ApiResponse.bad_request(f"😪 Lo siento, dificultades técnicas {entorno}")


@router.get("/version", tags=["DescripcionAPI"], summary="Versión del sistema")
async def version():
    return {
        "version": "1.0.0",
        "name": "Inventor-IA",
        "by": "BLACKTOWER"
    }