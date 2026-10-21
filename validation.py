def validate_product(data: dict) -> dict:
    name = data.get("name")
    category = data.get("category")
    price = data.get("price")
    stock = data.get("stock")

    if not isinstance(name, str) or not name.strip():
        raise ValueError("name is required and must be text")
    if not isinstance(category, str) or not category.strip():
        raise ValueError("category is required and must be text")
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price <= 0:
        raise ValueError("price must be a number greater than 0")
    if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
        raise ValueError("stock must be an integer of 0 or more")

    return {
        "name": name.strip(),
        "category": category.strip(),
        "price": float(price),
        "stock": stock,
    }