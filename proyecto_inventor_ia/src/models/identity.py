from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from bson import ObjectId

class RoleModel(BaseModel):
    name: str
    permissions: List[str] = []

class UserModel(BaseModel):
    email: EmailStr
    hashed_password: str
    role: Optional[str] = None
    is_active: bool = True
    reset_token: Optional[str] = None
