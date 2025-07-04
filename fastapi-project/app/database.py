# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URL")  # e.g. mongodb+srv://user:pass@cluster.mongodb.net/johnnyserver1

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.johnnyserver1
user_collection = database.get_collection("users")
