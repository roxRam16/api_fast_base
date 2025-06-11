from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = None

class UserOut(BaseModel):
    email: EmailStr
    role: Optional[str]

class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    email: EmailStr
    password: str

class ResetRequest(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str

class RoleCreate(BaseModel):
    name: str
    permissions: List[str]
