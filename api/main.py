from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PetData(BaseModel):
    health: float
    happiness: float
    type: str
    level: int

@app.get("/api/pet-data")
async def get_pet_data(authorization: str = Header(None)):
    # Здесь будет проверка авторизации и получение данных питомца
    return {
        "health": 80,
        "happiness": 90,
        "type": "cat",
        "level": 1
    }

@app.post("/api/feed")
async def feed_pet(authorization: str = Header(None)):
    # Здесь будет логика кормления питомца
    return {
        "health": 90,
        "happiness": 95,
        "type": "cat",
        "level": 1
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 