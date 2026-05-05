def check_quality(data: dict) -> list:
    """データ品質チェック（欠損・異常値）"""
    issues = []

    if data["price"] is None:
        issues.append("価格が取得できませんでした")

    if data["price"] is not None and data["price"] <= 0:
        issues.append("価格が0以下です")

    return issues
