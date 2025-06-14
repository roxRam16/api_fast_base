#LOGIN JWT - ROSARIO RAMIREZ RIOS

# MAYO 31 DEL 2025

#INVENTOR-IA

# Registro e inicio de sesión con JWT

# Roles y permisos (basado en scopes)

# CRUD de usuarios, roles y permisos

# Recuperación de contraseña mediante token (simulado por consola)

# Conexión a MongoDB (usando motor)

# Seguridad con OAuth2 + JWT


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config import Settings # nuestro settings.py con la variable APP_ENV
from src.routes.router import router as app_router
from src.routes.auth_router import router as app_auth
from src.routes.user_router import router as app_identity


# Define configuración común
app_config = {
    "title": "Inventor-IA : IDENTITY",
    "description": "Sistemas de inventarios con IA",
    "version": "1.0.0",
    "debug": Settings.APP_ENV,  # True para dev, False para prod
    # "openapi_tags": [
    #     {"name": "Inventario", "description": "Operaciones relacionadas con inventarios"},
    #     {"name": "Usuarios", "description": "Gestión de usuarios y autenticación"},
    #     {"name": "Pruebas", "description": "Endpoints de prueba y validación"},
    # ]
}

# En producción, desactiva la documentación
if not Settings.APP_ENV:
    app_config.update({
        "docs_url": None,
        "redoc_url": None,
        "openapi_url": None,
    })

# Instancia única de la app
app = FastAPI(**app_config)

# 🌐 CORS (ajústalo según tu frontend)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # "https://tudominio.com"  # en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # o ["*"] para todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🔌 Routers (define tus rutas en main.py y otros módulos)
app.include_router(app_router)
app.include_router(app_auth)
app.include_router(app_identity)

@app.get("/inventoria", tags=["DescripcionAPI"], summary="Versión del sistema")
async def version():
    return {
        "version": "1.0.0",
        "name": "Inventor-IA",
        "by": "ROXRAM"
    }


# 🔐 Redirección HTTP → HTTPS (si tienes un proxy inverso tipo Nginx)
# app.add_middleware(HTTPSRedirectMiddleware)

# 🧪 Middleware de seguridad extra (log de IPs, cabeceras, etc.)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    ip = request.client.host
    ua = request.headers.get("user-agent")
    print(f"🧾 Solicitud de {ip} - {ua}")
    response = await call_next(request)
    return response

#app.add_middleware(ExceptionHandlerMiddleware)


# ▶️ Punto de ejecución
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)