from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from ..services.auth_service import decode_token
from ..database.mongodb import MongoDB as db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ROLE_HIERARCHY = {
    "admin": ["admin", "editor", "viewer"],
    "editor": ["editor", "viewer"],
    "viewer": ["viewer"]
}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user = await db.get_collection_identity.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_roles_or_permissions(roles_allowed: list[str] = None, required_permissions: list[str] = None):
    roles_allowed = roles_allowed or []
    required_permissions = required_permissions or []

    async def checker(user=Depends(get_current_user)):
        role_name = user.get("role", "")
        if role_name in roles_allowed:
            return user

        role = await db.get_collection_roles.find_one({"name": role_name})
        if not role:
            raise HTTPException(status_code=403, detail="Role not found")

        user_permissions = set(role.get("permissions", []))
        if any(perm in user_permissions for perm in required_permissions):
            return user

        raise HTTPException(status_code=403, detail="Permission denied")

    return checker
