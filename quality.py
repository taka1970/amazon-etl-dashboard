def check_quality(data: dict) -> list:
    issues = []

    if data is None:
        issues.append("データが None")
        return issues

    if data["price"] is None:
        issues.append("価格が取得できていない")

    if data["title"] == "Unknown":
        issues.append("商品名が取得できていない")

    return issues
