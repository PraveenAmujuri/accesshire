import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

logger = logging.getLogger("accesshire.database")

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    logger.info("Initializing MongoDB connection to %s", settings.MONGODB_URL)
    try:
        db_instance.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=2000
        )
        db_instance.db = db_instance.client[settings.DATABASE_NAME]
        # Verify connection
        await db_instance.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB: database=%s", settings.DATABASE_NAME)
    except Exception as e:
        logger.warning(
            "Could not connect to MongoDB at %s (%s). Running in offline/disconnected mode.",
            settings.MONGODB_URL, e
        )

async def close_mongo_connection():
    if db_instance.client:
        logger.info("Closing MongoDB connection")
        db_instance.client.close()

def get_database():
    return db_instance.db
