from fastapi import FastAPI
from src.frontend_api import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Tikos Pipeline API is running"}
