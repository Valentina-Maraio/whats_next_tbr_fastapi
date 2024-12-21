from motor.motor_asyncio import AsyncIOMotorClient
import os

# Read MongoDB URI and database name from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "book_tbr_db")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is not set.")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]

# Collections
books_collection = db["books"]