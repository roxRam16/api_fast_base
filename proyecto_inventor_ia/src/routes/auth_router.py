from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token
from crud import *
from schemas import *
from utils import get_current_user, require_permission

app = FastAPI()

@app.post("/register", status_code=201)
async def register(user: UserCreate):
    if await get_user_by_email(user.email):
        raise HTTPException(400, "Email already registered")
    await create_user(user.dict())
    return {"msg": "User created"}

@app.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(data={"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/roles")
async def create_role_endpoint(role: RoleCreate, user=Depends(require_permission("manage_roles"))):
    await create_role(role.dict())
    return {"msg": "Role created"}

@app.get("/roles")
async def list_roles_endpoint(user=Depends(require_permission("view_roles"))):
    roles = await list_roles()
    return roles

@app.get("/me", response_model=UserOut)
async def read_users_me(current_user=Depends(get_current_user)):
    return {"email": current_user["email"], "role": current_user.get("role")}

@app.post("/forgot-password")
async def forgot_password(req: ResetRequest):
    user = await get_user_by_email(req.email)
    if not user:
        raise HTTPException(404, "User not found")
    token = await set_reset_token(req.email)
    print(f"🔐 Token de recuperación: {token}")
    return {"msg": "Check your email for password reset instructions (simulated)."}

@app.post("/reset-password")
async def reset_password_endpoint(req: ResetPassword):
    if await reset_password(req.token, req.new_password):
        return {"msg": "Password reset successful"}
    raise HTTPException(400, "Invalid token")
