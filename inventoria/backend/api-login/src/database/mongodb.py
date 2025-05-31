from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from config import settings

class MongoDB:
    _client: AsyncIOMotorClient = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            cls._client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                server_api=ServerApi("1")
            )
        return cls._client

    @classmethod
    def get_database(cls):
        return cls.get_client()[settings.MONGODB_DB]
    
    @classmethod
    def get_collection_identity(cls):
        return cls.get_database()[settings.MONGODB_COLLECTION_IDENTITY]
    
    @classmethod
    def get_collection_roles(cls):
        return cls.get_database()[settings.MONGODB_COLLECTION_ROLES]
    
    @classmethod
    def get_collection_permisos(cls):
        return cls.get_database()[settings.MONGODB_COLLECTION_PERMISOS]
    
    @classmethod
    def get_collection_logs(cls):
        return cls.get_database()[settings.MONGODB_COLLECTION_LOGS]

    @classmethod
    def close_client(cls):
        if cls._client:
            cls._client.close()
