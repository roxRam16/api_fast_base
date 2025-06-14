from fastapi import APIRouter,FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from config import Settings
from ..services.auth_service import create_access_token
from ..models.identity import *
from ..models.schemas import *
from ..services.user_service import *
from ..utils.auth_utils import *
from src.utils.response import ApiResponse
from src.utils.logger import logger


router = APIRouter(prefix="/inventoria/identity/user")

if Settings.APP_ENV == False:

    entorno = "Production"

else:

    entorno = "Development"

@router.post("/register", status_code=201, tags=["Identity"])

async def register(user: UserCreate):

    if await get_user_by_email(user.email):

        logger.info(f"Info:409 - EMAIL ALREADY REGISTERED")
        return ApiResponse.bad_request(f"🛑 Info:409 - EMAIL ALREADY REGISTERED")
    
    response_ = await create_user(user.model_dump())

    if response_:

        return ApiResponse.success(f"🟢 Info:201 - USER CREATED OK")
    
    else:

        return ApiResponse.bad_request(f"🛑 Info:402 - USER CREATED BAD")


@router.post("/roles", tags=["Identity"])
# async def create_role_endpoint(role: RoleCreate, 
#                                user=Depends(require_roles_or_permissions(roles_allowed=["admin"], required_permissions=["manage_roles"]))):
async def create_role_endpoint(role: RoleCreate):
    
    response_ = await create_role(role.model_dump())

    if response_:

        return ApiResponse.success(f"🟢 Info:201 - ROLE CREATED OK")
    
    else:

        return ApiResponse.bad_request(f"🛑 Info:402 - ROLE CREATED BAD")



@router.get("/roles", tags=["Identity"])
# async def list_roles_endpoint(user=Depends(require_roles_or_permissions("view_roles"))):
async def list_roles_endpoint():

    roles = await list_roles()

    print(roles)
    
    return roles