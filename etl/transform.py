from datetime import datetime

def transform_price(raw: dict, url: str) -> dict:
    if raw is None:
        return None

    return {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": url,
        "title": raw["title"],
        "price": raw["price"]
    }
