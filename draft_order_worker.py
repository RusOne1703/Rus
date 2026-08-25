import os
import json
import time
import logging
import urllib.request
import urllib.error
import html
from pathlib import Path
from datetime import datetime

# Настройки логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Конфигурация Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')

# Конфигурация директории и таймаута
DRAFT_DIR = Path('.data/draft-orders')
# Время, после которого корзина считается "брошенной" (в секундах). Например, 30 минут = 1800 сек.
ABANDONED_THRESHOLD_SEC = 1800

def send_telegram_alert(draft_data):
    """Отправляет уведомление менеджерам в Telegram (без сторонних зависимостей)."""

    # Извлекаем и экранируем данные, чтобы не сломать HTML parse_mode Telegram'а
    phone = html.escape(str(draft_data.get('customer_phone', 'Не указан')))
    telegram = html.escape(str(draft_data.get('customer_telegram', 'Не указан')))

    # Ссылку нужно экранировать как для атрибута href, так и для текста, но urllib справляется,
    # однако амперсанды в URL могут сломать HTML-парсер, если вставлять как текст.
    raw_link = str(draft_data.get('product_link', 'Не указано'))
    product_link = html.escape(raw_link)

    product_name = html.escape(str(draft_data.get('product_name', 'Не указано')))
    size = html.escape(str(draft_data.get('size', 'Не указано')))
    created_at = html.escape(str(draft_data.get('created_at', 'Неизвестно')))

    text = (
        "🚨 <b>Брошенная корзина!</b>\n\n"
        f"📱 <b>Телефон:</b> {phone}\n"
        f"✈️ <b>Telegram:</b> {telegram}\n\n"
        f"👟 <b>Товар:</b> {product_name}\n"
        f"📏 <b>Размер:</b> {size}\n"
        f"🔗 <b>Ссылка:</b> <a href='{product_link}'>Poizon Link</a>\n\n"
        f"🕒 <i>Создано: {created_at}</i>\n\n"
        "👉 Свяжитесь с клиентом в WhatsApp/Telegram и предложите помощь с оформлением!"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return True
            else:
                logging.error(f"Неожиданный статус от Telegram: {response.status}")
                return False
    except urllib.error.HTTPError as e:
        error_info = e.read().decode('utf-8')
        logging.error(f"HTTP Ошибка от Telegram: {e.code} - {error_info}")
        return False
    except urllib.error.URLError as e:
        logging.error(f"Ошибка сети/соединения с Telegram: {e.reason}")
        return False
    except Exception as e:
        logging.error(f"Неизвестная ошибка при отправке в Telegram: {e}")
        return False

def process_abandoned_carts():
    """Сканирует директорию с драфтами и отправляет алерты."""
    if not DRAFT_DIR.exists():
        logging.warning(f"Директория {DRAFT_DIR} не существует. Выход.")
        return

    now = time.time()
    processed_count = 0

    for filepath in DRAFT_DIR.glob('*.json'):
        file_mtime = filepath.stat().st_mtime

        if (now - file_mtime) >= ABANDONED_THRESHOLD_SEC:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    draft_data = json.load(f)

                if 'created_at' not in draft_data:
                    dt_object = datetime.fromtimestamp(file_mtime)
                    draft_data['created_at'] = dt_object.strftime('%Y-%m-%d %H:%M:%S')

                logging.info(f"Найдена брошенная корзина: {filepath.name}")

                if send_telegram_alert(draft_data):
                    filepath.unlink()
                    logging.info(f"Файл {filepath.name} успешно обработан и удален.")
                    processed_count += 1
                else:
                    logging.error(f"Не удалось отправить алерт для {filepath.name}. Файл сохранен для следующего запуска.")

            except json.JSONDecodeError:
                logging.error(f"Ошибка чтения JSON из файла {filepath.name}. Файл поврежден.")
            except Exception as e:
                logging.error(f"Непредвиденная ошибка при обработке {filepath.name}: {e}")

    logging.info(f"Сканирование завершено. Обработано корзин: {processed_count}")

if __name__ == "__main__":
    logging.info("Запуск воркера брошенных корзин...")
    process_abandoned_carts()
