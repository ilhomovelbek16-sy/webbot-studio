import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests

app = FastAPI()

# ⚠️ O'zingizning bot tokeningiz va chat ID raqamingizni shu yerga yozing
# (Yoki Render'da Environment Variables ga qo'shgan bo'lsangiz o'zicha o'qiydi)
BOT_TOKEN = os.getenv("9258223617:AAHrUny-WK-tP3zGsjEaSWRe1F2y0hO9h9Q")
CHAT_ID = os.getenv("7135553744")


class Order(BaseModel):
  name: str
  phone: str
  project_type: str
  total_price: str


# 1. Asosiy sahifada index.html faylini ochish (MUHIM QISM)
@app.get("/")
async def serve_index():
  return FileResponse("index.html")


# 2. Buyurtmani qabul qilib Telegramga yuborish
@app.post("/api/order")
async def create_order(order: Order):
  message = (
      f"🔔 <b>Yangi buyurtma keldi!</b>\n\n"
      f"👤 <b>Ism:</b> {order.name}\n"
      f"📞 <b>Telefon:</b> {order.phone}\n"
      f"💻 <b>Loyiha turi:</b> {order.project_type}\n"
      f"💰 <b>Narxi:</b> {order.total_price}"
  )

  url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}

  try:
    response = requests.post(url, json=payload)
    if response.status_code != 200:
      raise HTTPException(
          status_code=500, detail="Telegramga xabar yuborishda xatolik"
      )
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Server xatoligi: {str(e)}")

  return {"status": "success", "message": "Buyurtma qabul qilindi"}