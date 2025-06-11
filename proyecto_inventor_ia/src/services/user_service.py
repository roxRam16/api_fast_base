from database import db
from services.auth_service import hash_password, verify_password
from bson import ObjectId
import uuid

async def create_user(user_data):
    user_data["hashed_password"] = hash_password(user_data.pop("password"))
    await db.users.insert_one(user_data)

async def get_user_by_email(email):
    return await db.users.find_one({"email": email})

async def get_role(name):
    return await db.roles.find_one({"name": name})

async def create_role(role_data):
    await db.roles.insert_one(role_data)

async def list_roles():
    return await db.roles.find().to_list(100)

async def authenticate_user(email, password):
    user = await get_user_by_email(email)
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None

async def set_reset_token(email):
    token = str(uuid.uuid4())
    await db.users.update_one({"email": email}, {"$set": {"reset_token": token}})
    return token

async def reset_password(token, new_password):
    hashed = hash_password(new_password)
    result = await db.users.update_one(
        {"reset_token": token},
        {"$set": {"hashed_password": hashed}, "$unset": {"reset_token": ""}}
    )
    return result.modified_count > 0
