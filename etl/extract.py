import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7"
}

def extract_price(url: str) -> dict:
    """Amazon商品ページから商品名と価格を抽出"""
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # 商品名
        title_tag = soup.find("span", {"id": "productTitle"})
        title = title_tag.get_text().strip() if title_tag else "Unknown"

        # 価格
        price_tag = soup.find("span", {"class": "a-offscreen"})
        price = None
        if price_tag:
            price_text = price_tag.get_text()
            price = int(re.sub(r"\D", "", price_text))

        return {
            "url": url,      # ← 必須
            "title": title,  # ← 必須
            "price": price   # ← 必須
        }

    except Exception as e:
        print(f"Extract error: {e}")
        return None
