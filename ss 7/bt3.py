# Input

# API sử dụng phương thức:

# POST /orders

# Dữ liệu gửi lên (JSON):

# {
#     "product_id": 101,
#     "quantity": 2
# }

# Schema:

# Thuộc tính	Kiểu dữ liệu	Ý nghĩa
# product_id	int	Mã sản phẩm
# quantity	int	Số lượng mua
# Output khi thành công

# HTTP Status:

# 201 Created

# Sau khi tạo đơn:

# thêm đơn hàng vào orders_db
# giảm số lượng tồn kho của sản phẩm
# Output khi thất bại
# Trường hợp 1

# Sản phẩm không tồn tại

# 404 Not Found
# {
#     "detail": "Không tìm thấy sản phẩm"
# }
# Trường hợp 2

# Số lượng <=0

# 400 Bad Request
# {
#     "detail": "Số lượng mua phải lớn hơn 0"
# }
# Trường hợp 3

# Đặt vượt tồn kho

# 400 Bad Request
# {
#     "detail": "Sản phẩm không đủ số lượng trong kho"
# }

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]
orders_db = []

class OrderCreate(BaseModel):
    product_id: int
    quantity: int 

@app.post("/orders",status_code=status.HTTP_201_CREATED)
def create_order(order:OrderCreate):
    if order.quantity <= 0 :
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="số lượng mua phải lớn hơn 0"
        )
    
    product = None

    for i in products_db:
        if i["id"] == order.product_id:
            product = i 
            break
    if product is None :
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KHÔNG TÌM THẤY SẢN PHẨM"
        )
    
    if order.quantity > product["stock"] :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Snar phẩm không đủ số lượng trong kho"
        )
    
    product["stock"] -=order.quantity

    total_price = order.quantity * product["price"]

    new_order = {
        "order_id" : len(orders_db) +1,
        "product_id": order.product_id,
        "quantity" :order.quantity,
        "total_price" : total_price
    }

    orders_db.append(new_order)

    return {
        "message": "Tạo đơn hàng thành công",
        "order": new_order
    }

@app.get("/products")
def get_products():
    return {
        "products": products_db
    }