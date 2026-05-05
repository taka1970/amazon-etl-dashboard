from etl.extract import extract_price
from etl.transform import transform_price
from etl.load import insert_price, init_db
from etl.quality import check_quality
from etl.logger import log_info, log_error

# 複数商品URL
URLS = [
    "https://www.amazon.co.jp/dp/B07Q8TJ2KL",
    "https://www.amazon.co.jp/dp/B0CGLV7Z8P",
    "https://www.amazon.co.jp/dp/B09V3HN1V7"
]

def run_etl():
    log_info("=== ETL開始 ===")

    for url in URLS:
        log_info(f"処理開始: {url}")

        raw = extract_price(url)
        if raw is None:
            log_error(f"抽出失敗: {url}")
            continue

        data = transform_price(raw, url)

        issues = check_quality(data)
        if issues:
            log_error(f"品質エラー: {issues} | URL: {url}")
            continue

        insert_price(data)
        log_info(f"保存完了: {data}")

    log_info("=== ETL完了 ===")

if __name__ == "__main__":
    init_db()
    run_etl()
