# Инструкция по развертыванию Backend API (Sotrue Hotfix)

В этой директории `backend/` находится готовый каркас микросервиса на **FastAPI**, который реализует весь отложенный функционал из `AUDIT_ROADMAP.md`.

## Что реализовано:
1. **On-demand парсинг цен (Playwright + Redis)** — эндпоинт `GET /api/price/{slug}` динамически парсит цену, кэширует ее на 1 час и отдает на фронт.
2. **База данных (PostgreSQL)** — ORM модели для товаров и заказов (`models.py`).
3. **Хранилище картинок (S3)** — клиент для работы с Yandex Object Storage/AWS S3 (`s3_storage.py`).
4. **Умный поиск (Meilisearch)** — интеграция с высокоскоростным движком поиска (`search.py`).
5. **Трекинг доставки (СДЭК/Boxberry)** — интеграция с API транспортных компаний (`delivery.py`).

## Инструкция по запуску на вашем сервере (Production)

### 1. Настройте переменные окружения (ОБЯЗАТЕЛЬНО)
В целях безопасности, базы данных и кэш не имеют стандартных паролей.
Скопируйте пример конфига и установите **СВОИ, СЛОЖНЫЕ ПАРОЛИ**:
```bash
cd backend
cp .env.example .env
nano .env
```
Обязательно сгенерируйте новые значения для `POSTGRES_PASSWORD`, `REDIS_PASSWORD` и `MEILI_MASTER_KEY`. В этом же файле укажите ваши ключи СДЭК и S3.

### 2. Поднимите инфраструктуру
Вернитесь в корень проекта, где лежит `docker-compose.yml`. Он поднимет БД, Redis и Meilisearch, используя пароли из вашего `.env` файла. Порты безопасно проброшены только на `127.0.0.1`.
```bash
cd ..
docker-compose --env-file backend/.env up -d
```

### 3. Запуск API
Создайте виртуальное окружение и установите зависимости:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Для деплоя на проде рекомендуется использовать `uvicorn` с менеджером процессов, например, `systemd` или `supervisor`.
Перед запуском убедитесь, что переменные из `.env` загружены в окружение. Вы можете использовать пакет `python-dotenv` или загрузить их через bash:
```bash
export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
uvicorn main:app --host 127.0.0.1 --port 8000
```

### 4. Настройка Nginx
Если ваш фронтенд работает на Nginx, проксируйте запросы `/api` к вашему новому FastAPI приложению:
```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

Готово! Теперь ваш фронтенд сможет дергать рабочий эндпоинт `GET /api/price/{slug}`.