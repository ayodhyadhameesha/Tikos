from fastapi import APIRouter, HTTPException
from connections.database import collection

router = APIRouter()

# This endpoint is used by the frontend to get all users
@router.get("/users")
async def get_all_users():
    try:
        docs = await collection.find().to_list(100)
        
        for doc in docs:
            doc["_id"] = str(doc["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
