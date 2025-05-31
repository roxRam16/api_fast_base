#📦 Estructura de respuesta estándar

# {
#   "status": "success" | "error",
#   "code": 200,
#   "message": "Texto descriptivo",
#   "data": {} | null
# }


from fastapi.responses import JSONResponse
from fastapi import status


class ApiResponse:
    @staticmethod
    def success(message: str = "Operación exitosa", data=None, code: int = status.HTTP_200_OK):
        return JSONResponse(
            status_code=code,
            content={
                "status": "success",
                "code": code,
                "message": message,
                "data": data
            }
        )

    @staticmethod
    def created(message: str = "Recurso creado exitosamente", data=None):
        return ApiResponse.success(message, data, code=status.HTTP_201_CREATED)

    @staticmethod
    def no_content():
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content=None
        )

    @staticmethod
    def error(message: str = "Ocurrió un error", code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, data=None):
        return JSONResponse(
            status_code=code,
            content={
                "status": "error",
                "code": code,
                "message": message,
                "data": data
            }
        )

    @staticmethod
    def bad_request(message: str = "Solicitud inválida", data=None):
        return ApiResponse.error(message, code=status.HTTP_400_BAD_REQUEST, data=data)

    @staticmethod
    def unauthorized(message: str = "No autenticado", data=None):
        return ApiResponse.error(message, code=status.HTTP_401_UNAUTHORIZED, data=data)

    @staticmethod
    def forbidden(message: str = "Acceso denegado", data=None):
        return ApiResponse.error(message, code=status.HTTP_403_FORBIDDEN, data=data)

    @staticmethod
    def not_found(message: str = "Recurso no encontrado", data=None):
        return ApiResponse.error(message, code=status.HTTP_404_NOT_FOUND, data=data)

    @staticmethod
    def conflict(message: str = "Conflicto de datos", data=None):
        return ApiResponse.error(message, code=status.HTTP_409_CONFLICT, data=data)

    @staticmethod
    def unprocessable(message: str = "Datos no válidos", data=None):
        return ApiResponse.error(message, code=status.HTTP_422_UNPROCESSABLE_ENTITY, data=data)
