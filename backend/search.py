import meilisearch
import os

MEILI_URL = os.getenv("MEILI_URL", "http://localhost:7700")
MEILI_MASTER_KEY = os.getenv("MEILI_MASTER_KEY", "your_secure_master_key_here")

# Инициализация клиента Meilisearch
client = meilisearch.Client(MEILI_URL, MEILI_MASTER_KEY)

def setup_search_index():
    """
    Создает индекс и настраивает параметры умного поиска.
    """
    index = client.index('products')

    # Настройка полей, по которым будет идти полнотекстовый поиск
    index.update_searchable_attributes([
        'title',
        'brand',
        'category'
    ])

    # Настройка фильтров (например, для фасетного поиска на фронте)
    index.update_filterable_attributes([
        'brand',
        'category'
    ])

    print("[Meilisearch] Индекс 'products' успешно настроен.")

def index_product(product_data: dict):
    """
    Добавляет или обновляет товар в поисковом индексе.
    product_data должен содержать: id, title, brand, category, image_url.
    """
    client.index('products').add_documents([product_data])

def search_products(query: str, limit: int = 10):
    """
    Выполняет умный морфологический поиск.
    """
    result = client.index('products').search(query, {
        'limit': limit
    })
    return result['hits']
