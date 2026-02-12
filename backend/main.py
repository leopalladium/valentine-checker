from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()

# Настройка CORS (разрешаем запросы с фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["klimentsi.live"],  # В идеале тут должен быть твой домен, но "*" сойдет для старта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResponseModel(BaseModel):
    answer: str

@app.post("/api/response")
async def save_response(data: ResponseModel):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"❤️ SHE SAID YES! Time: {now}")
    # Тут можно подключить Telegram бота, если захочешь позже
    return {"status": "success", "message": "Love is in the air!"}

@app.get("/api/health")
async def health():
    return {"status": "ok"}