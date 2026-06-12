from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client: AsyncIOMotorClient = None
db = None


async def connect_mongodb():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB_NAME]
    print(f"âœ… MongoDB connected: {settings.MONGODB_DB_NAME}")


async def close_mongodb():
    global client
    if client:
        client.close()


def get_db():
    return db
