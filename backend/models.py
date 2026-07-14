from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    poizon_id = Column(String, unique=True, index=True) # Оригинальный ID с Poizon
    slug = Column(String, unique=True, index=True)      # Человекопонятный URL для SEO
    title = Column(String, index=True)
    brand = Column(String, index=True)
    category = Column(String)
    image_url = Column(String) # URL картинки в нашем S3
    base_price_yuan = Column(Float, nullable=True) # Базовая цена, обновляемая парсером
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True) # ID пользователя из внешней системы авторизации
    product_poizon_id = Column(String)
    size = Column(String)
    final_price_rub = Column(Float)
    status = Column(String, default="PENDING") # PENDING, BUYING, LEGIT_CHECK, SHIPPED_TO_RU, DELIVERED
    tracking_number = Column(String, nullable=True) # Трек номер СДЭК/Boxberry
    created_at = Column(DateTime(timezone=True), server_default=func.now())
