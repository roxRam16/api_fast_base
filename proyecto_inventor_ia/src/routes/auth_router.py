from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from config import Settings
from ..services.auth_service import create_access_token
from ..models.identity import *
from ..models.schemas import *
from ..services.user_service import *
from ..utils.auth_utils import *


router = APIRouter(prefix="/inventoria/auth")

if Settings.APP_ENV == False:

    entorno = "Production"

else:

    entorno = "Development"
    

@router.post("/login", response_model=Token, tags=["Auth"])
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user = await authenticate_user(form.username, form.password)

    if not user:

        logger.info(f"Info:401 - INVALID CREDENTIALS")
        return ApiResponse.bad_request(f"🛑 Info:401 - INVALID CREDENTIALS")
    
    token = create_access_token(data={"sub": user["email"]})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut, tags=["Auth"])
async def read_users_me(current_user=Depends(get_current_user)):
    return {"email": current_user["email"], "role": current_user.get("role")}


@router.post("/forgot-password", tags=["Auth"])
async def forgot_password(req: ResetRequest):

    user = await get_user_by_email(req.email)

    if not user:

        logger.info(f"Info:404 - USER NOT FOUND")
        return ApiResponse.bad_request(f"🛑 404 - USER NOT FOUND")
   
    token = await set_reset_token(req.email)

    #implementar para instrucciones al correo
    print(f"🔐 Token de recuperación: {token}")
    return {"msg": "Check your email for password reset instructions (simulated)."}


@router.post("/reset-password", tags=["Auth"])
async def reset_password_endpoint(req: ResetPassword):

    if await reset_password(req.token, req.new_password):
        logger.info(f"Info:201 - CONTRASEÑA RESTAURADA OK")
        return ApiResponse.success(f"🟢 Info:201 - CONTRASEÑA RESTAURADA OK")
    
    logger.info(f"Info:400 - EMAIL ALREADY REGISTERED")
    raise HTTPException(400, "Invalid token")
