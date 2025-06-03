from fastapi import APIRouter, HTTPException, Depends
from db import get_connection
from jose import jwt, JWTError
from auth import SECRET_KEY, ALGORITHM
from utils.token import oauth2_scheme
from schemas import StatusUpdate
from utils.roles import require_admin

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order(order: dict, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        items = order.get("items", [])
        if not items:
            raise HTTPException(status_code=400, detail="Order must contain items")

        total_price = sum(item["quantity"] * item["price"] for item in items)

        cursor.execute("INSERT INTO orders (user_id, total_price, status) VALUES (%s, %s, %s)",
                       (user["id"], total_price, "pending"))
        order_id = cursor.lastrowid

        for item in items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item["product_id"], item["quantity"], item["price"]))

        conn.commit()
        return {"message": "Order placed successfully", "order_id": order_id}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    finally:
        cursor.close()
        conn.close()


@router.get("/")
def get_user_orders(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user["id"],))
        orders = cursor.fetchall()
        return {"orders": orders}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    finally:
        cursor.close()
        conn.close()


@router.get("/{order_id}")
def get_order_detail(order_id: int, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        cursor.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s", (order_id, user["id"]))
        order = cursor.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        cursor.execute("""
            SELECT 
                oi.product_id, 
                p.name AS product_name,
                p.image_url,
                oi.quantity,
                oi.price
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """, (order_id,))
        items = cursor.fetchall()

        return {"order": order, "items": items}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    finally:
        cursor.close()
        conn.close()


@router.put("/{order_id}/status")
def update_order_status(order_id: int, status_update: StatusUpdate, token: str = Depends(oauth2_scheme)):
    require_admin(token)

    conn = get_connection()
    cursor = conn.cursor()

    valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (status_update.status, order_id))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": f"Order status updated to '{status_update.status}'"}
