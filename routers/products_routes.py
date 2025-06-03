from fastapi import APIRouter, HTTPException, Depends
from db import get_connection
from utils.token import oauth2_scheme
from utils.roles import require_admin

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def list_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"products": products}

@router.get("/{product_id}")
def get_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ✅ Admin-only endpoint
@router.post("/")
def add_product(product: dict, token: str = Depends(oauth2_scheme)):
    require_admin(token)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, description, image_url, price, category)
        VALUES (%s, %s, %s, %s, %s)
    """, (product["name"], product["description"], product["image_url"], product["price"], product["category"]))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Product added"}

# ✅ Admin-only endpoint
@router.put("/{product_id}")
def update_product(product_id: int, product: dict, token: str = Depends(oauth2_scheme)):
    require_admin(token)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products SET name=%s, description=%s, image_url=%s, price=%s, category=%s
        WHERE id=%s
    """, (product["name"], product["description"], product["image_url"], product["price"], product["category"], product_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Product updated"}

# ✅ Admin-only endpoint
@router.delete("/{product_id}")
def delete_product(product_id: int, token: str = Depends(oauth2_scheme)):
    require_admin(token)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Product deleted"}
