from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from datetime import datetime
from typing import Optional

import os
from dotenv import load_dotenv
load_dotenv()


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "agentic_poc")


client: Optional[MongoClient] = None
db: Optional[AsyncIOMotorClient] = None
def init_db():
    global client, db
    if client is None:
        client = MongoClient(MONGO_URI) 
        db=client[MONGO_DB_NAME]


def get_db()-> AsyncIOMotorClient:
    if db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return db

      