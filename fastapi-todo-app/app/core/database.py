"""Database connection and configuration."""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

from app.core.config import settings


class Database:
    """Database connection manager."""
    
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None


# Global database instance
db = Database()


async def connect_to_mongo() -> None:
    """
    Create database connection.
    
    Establishes connection to MongoDB and sets up the database instance.
    """
    try:
        db.client = AsyncIOMotorClient(settings.mongodb_url)
        db.database = db.client[settings.database_name]
        
        # Test the connection
        await db.client.admin.command('ping')
        print(f"Successfully connected to MongoDB at {settings.mongodb_url}")
        
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection() -> None:
    """
    Close database connection.
    
    Properly closes the MongoDB connection when the application shuts down.
    """
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")


def get_database() -> AsyncIOMotorDatabase:
    """
    Get database instance.
    
    Returns:
        AsyncIOMotorDatabase: The MongoDB database instance.
        
    Raises:
        RuntimeError: If database connection is not established.
    """
    if db.database is None:
        raise RuntimeError("Database connection not established")
    return db.database
