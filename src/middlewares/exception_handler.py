from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.response import ApiResponse


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except RequestValidationError as e:
            # Validación de datos (422)
            return ApiResponse.unprocessable("Error de validación de datos", data=e.errors())
        except StarletteHTTPException as e:
            # Excepciones HTTP de FastAPI (como 404, 403, etc.)
            return ApiResponse.error(message=e.detail, code=e.status_code)
        except Exception as e:
            # Errores no controlados (500)
            return ApiResponse.error(message="Error interno del servidor", data={"error": str(e)})
