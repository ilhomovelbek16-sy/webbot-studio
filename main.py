from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shu yerdagi so'zlar o'rniga o'zingizning haqiqiy Bot Token va Chat ID ingizni yozing:
BOT_TOKEN = "9258223617:AAHrUny-WK-tP3zGsjEaSWRe1F2y0hO9h9Q"
CHAT_ID = "7135553744"

class OrderSchema(BaseModel):
    name: str
    phone: str
    project_type: str
    total_price: str

@app.post("/api/order")
def create_order(order: OrderSchema):
    if not order.name or not order.phone:
        raise HTTPException(status_code=400, detail="Ism va telefon raqami kiritilishi shart!")
    
    text = (
        f"Yangi buyurtma keldi!\n\n"
        f"Mijoz: {order.name}\n"
        f"Telefon: {order.phone}\n"
        f"Loyiha turi: {order.project_type}\n"
        f"Narxi: {order.total_price}"
    )
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print("Telegram javobi:", response.text)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Telegram xatosi: {response.text}")
                    
    except requests.exceptions.RequestException as e:
        print("Tarmoq ulanishida xatolik:", str(e))
        raise HTTPException(status_code=500, detail=f"Internetga ulanib bo'lmadi: {str(e)}")
    
    return {"status": "success", "message": "Buyurtma muvaffaqiyatli qabul qilindi!"}
from fastapi.staticfiles import StaticFiles

# Bu qator index.html va boshqa fayllarni internetga chiqaradi
app.mount("/", StaticFiles(directory=".", html=True), name="static")
from fastapi.responses import FileResponse


@app.get("/")
async def read_index():
  return FileResponse("index.html")