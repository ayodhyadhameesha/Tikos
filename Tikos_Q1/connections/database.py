from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
client = AsyncIOMotorClient('mongodb://localhost:27017/')

# Database and collection
db = client["tikos_pipeline"]
collection = db["users"]
