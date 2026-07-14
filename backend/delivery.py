import requests
import os

SDEK_CLIENT_ID = os.getenv("SDEK_CLIENT_ID", "your_cdek_client_id")
SDEK_CLIENT_SECRET = os.getenv("SDEK_CLIENT_SECRET", "your_cdek_client_secret")

def get_cdek_token() -> str:
    """Получает Bearer токен для API СДЭК v2."""
    url = "https://api.cdek.ru/v2/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": SDEK_CLIENT_ID,
        "client_secret": SDEK_CLIENT_SECRET
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
    except Exception as e:
        print(f"[CDEK Auth Error] {e}")
    return None

def track_cdek_order(tracking_number: str) -> dict:
    """
    Получает текущий статус посылки по трек-номеру.
    """
    token = get_cdek_token()
    if not token:
        return {"error": "Authentication failed"}

    url = f"https://api.cdek.ru/v2/orders?cdek_number={tracking_number}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Упрощаем ответ для нашего фронтенда
            if data and "entity" in data:
                statuses = data["entity"].get("statuses", [])
                latest_status = statuses[-1] if statuses else None
                return {
                    "tracking_number": tracking_number,
                    "latest_status_code": latest_status.get("code") if latest_status else "UNKNOWN",
                    "latest_status_name": latest_status.get("name") if latest_status else "Неизвестно"
                }
    except Exception as e:
        print(f"[CDEK Tracking Error] {e}")

    return {"error": "Could not fetch tracking info"}

# Аналогично реализуется интеграция с API Boxberry
def track_boxberry_order(tracking_number: str) -> dict:
    # Заглушка для Boxberry
    return {
        "tracking_number": tracking_number,
        "latest_status_name": "В пути (Boxberry Fallback)"
    }
