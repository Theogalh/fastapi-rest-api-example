import os
import motor.motor_asyncio

MONGO_DETAILS = "mongodb://mongodb" if os.environ.get(
    'PLATFORM', "local") == "docker" else "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

db = client.octogone_project
