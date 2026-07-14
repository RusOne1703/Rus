from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
import redis
import json
import os

from database import engine, Base, get_db
import models
import scraper
import search
import delivery

# Инициализация БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sotrue API", description="Backend для маркетплейса sotrue.ru")

# Инициализация Redis для кэширования on-demand цен
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
if not REDIS_PASSWORD:
     raise ValueError("REDIS_PASSWORD environment variable is not set. Please check your .env file.")

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True, password=REDIS_PASSWORD)

class ProductResponse(BaseModel):
    id: int
    poizon_id: str
    title: str
    price_rub: float

    class Config:
        orm_mode = True

# Курс валют (в идеале тянуть по API)
YUAN_TO_RUB = 13.5
COMMISSION = 2000 # Комиссия сервиса
DELIVERY_COST = 1500 # Фиксированная стоимость доставки из Китая

@app.get("/api/price/{slug}")
async def get_dynamic_price(slug: str, db: Session = Depends(get_db)):
    """
    On-demand парсинг цены товара. Если цена есть в кэше — отдаем мгновенно.
    Если нет — парсим, сохраняем в Redis на час и отдаем.
    """
    product = db.query(models.Product).filter(models.Product.slug == slug).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cache_key = f"price_{product.poizon_id}"
    cached_price = redis_client.get(cache_key)

    if cached_price:
        yuan_price = float(cached_price)
        print(f"[Cache Hit] Цена для {product.poizon_id} извлечена из Redis")
    else:
        # Дергаем Playwright парсер
        yuan_price = await scraper.scrape_poizon_price(product.poizon_id)
        if yuan_price is None:
            # Fallback - берем последнюю известную цену из БД
            yuan_price = product.base_price_yuan or 0.0
        else:
            # Обновляем БД и Кэш
            product.base_price_yuan = yuan_price
            db.commit()
            redis_client.setex(cache_key, 3600, yuan_price) # Кэш на 1 час
            print(f"[Scraped] Цена для {product.poizon_id} спарсена и закэширована")

    # Формула расчета конечной стоимости
    final_price_rub = (yuan_price * YUAN_TO_RUB) + COMMISSION + DELIVERY_COST

    return {
        "poizon_id": product.poizon_id,
        "title": product.title,
        "base_price_yuan": yuan_price,
        "final_price_rub": round(final_price_rub, 2)
    }

@app.get("/api/search")
def search_catalog(q: str):
    """Умный поиск через Meilisearch"""
    results = search.search_products(q)
    return {"query": q, "results": results}

@app.get("/api/track/{tracking_number}")
def track_order(tracking_number: str, carrier: str = "cdek"):
    """Трекинг заказов"""
    if carrier == "cdek":
        return delivery.track_cdek_order(tracking_number)
    elif carrier == "boxberry":
        return delivery.track_boxberry_order(tracking_number)
    else:
        raise HTTPException(status_code=400, detail="Unsupported carrier")
