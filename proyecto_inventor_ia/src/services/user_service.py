from ..database.mongodb import MongoDB
from ..services.auth_service import hash_password, verify_password
from bson import ObjectId
import uuid
from datetime import datetime, timedelta
from src.utils.response import ApiResponse
from src.utils.logger import logger


async def create_user(user_data):

    try:
        # Hashear password y eliminar campo 'password'
        plain_password = user_data.pop("password", None)

        if not plain_password:
            raise ValueError("Password is required")
        
        user_data["hashed_password"] = hash_password(plain_password)
        
        # Asignar un _id si quieres (opcional)
        user_data["_id"] = ObjectId()

        # Insertar en colección identidad
        collection = MongoDB.get_collection_identity()

        result = await collection.insert_one(user_data)

        if result :

            logger.info(f"Info:201 - USER CREATED OK")
            return True
        
        else:

            logger.info(f"Info:402 - USER CREATED BAD")
            return False
        
    except Exception as e:
          logger.info(f"Info:402 - USER CREATED BAD: {e}")
          return False
    

async def get_user_by_email(email):

    collection = MongoDB.get_collection_identity()

    return await collection.find_one({"email": email})


async def get_role(name):

    collection = MongoDB.get_collection_roles()

    return await collection.find_one({"name": name})


async def create_role(role_data):

    collection = MongoDB.get_collection_roles()

    result = await collection.insert_one(role_data)

    return str(result.inserted_id)



async def list_roles():

    try:

        collection = MongoDB.get_collection_roles()

        roles = collection.find().to_list(100)

        for rol in roles:
            rol["_id"] = str(rol["_id"])
        
        return roles
    
    except Exception as e:
        logger.info(f"Info:402 - ROLES NOT FOUND: {e}")
        return False


async def authenticate_user(email, password):

    user = await get_user_by_email(email)

    if user and verify_password(password, user["hashed_password"]):

        return user
    
    return None


async def set_reset_token(email):

    user = await get_user_by_email(email)

    if not user:

        return None
    
    token = str(uuid.uuid4())

    expire_at = datetime.now() + timedelta(hours=1)

    collection = MongoDB.get_collection_identity()

    await collection.update_one({"email": email}, {"$set": {"reset_token": token, "reset_token_expire": expire_at}})

    return token


async def reset_password(token, new_password):

    now = datetime.now()

    collection = MongoDB.get_collection_identity()
    
    user = await collection.find_one({
        "reset_token": token,
        "reset_token_expire": {"$gt": now}
    })

    if not user:
        return False
    
    hashed = hash_password(new_password)

    result = await collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"hashed_password": hashed}, "$unset": {"reset_token": "", "reset_token_expire": ""}}
    )

    return result.modified_count > 0
