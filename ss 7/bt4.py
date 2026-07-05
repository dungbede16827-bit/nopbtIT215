# Input

# API:

# GET /orders/{order_id}/payment

# Trong đó:

# order_id: kiểu số nguyên (int)
# Là ID của đơn hàng cần tra cứu.
# Output thành công

# HTTP Status:

# 200 OK

# Response

# {
#     "message": "Lấy thông tin thanh toán thành công",
#     "data": {
#         "id": 1,
#         "code": "SP001",
#         "payment_status": "PAID",
#         "method": "BANK_TRANSFER"
#     }
# }
# Output thất bại
# Trường hợp 1: Không tìm thấy đơn hàng

# HTTP Status

# 404 Not Found

# Response

# {
#     "detail": "Không tìm thấy đơn hàng"
# }
# Trường hợp 2: Lỗi hệ thống

# HTTP Status

# 500 Internal Server Error

# Response

# {
#     "detail": "Hệ thống đang gặp sự cố, vui lòng thử lại sau."
# }
# Giải pháp 1 - Lưu dữ liệu bằng List

# Cách tìm kiếm

# Duyệt từng phần tử trong danh sách.
# Giải pháp 2 - Lưu dữ liệu bằng Dict
# Cách tìm kiếm
# order = orders_dict.get(order_id)
# Đối với hệ thống thương mại điện tử mỗi ngày phát sinh hàng chục nghìn đơn hàng, Dict là lựa chọn tối ưu vì:

# Tra cứu rất nhanh.
# Không cần duyệt toàn bộ dữ liệu.
# Giảm độ trễ (Latency).
# Phù hợp với hệ thống có lượng truy cập lớn.
# Dễ mở rộng khi tích hợp cơ sở dữ liệu.

from fastapi import FastAPI, HTTPException

app = FastAPI()
orders = {
    1: {
        "id": 1,
        "code": "SP001",
        "payment_status": "PAID",
        "method": "BANK_TRANSFER"
    },
    2: {
        "id": 2,
        "code": "SP002",
        "payment_status": "UNPAID",
        "method": "NONE"
    }
}
@app.get("/orders/{order_id}/payment")
def get_payment(order_id: int):
    try:
        order = orders.get(order_id)
        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Không tìm thấy đơn hàng"
            )

        return {
            "message": "Lấy thông tin thanh toán thành công",
            "data": {
                "id": order["id"],
                "code": order["code"],
                "payment_status": order["payment_status"],
                "method": order["method"]
            }
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Hệ thống đang gặp sự cố, vui lòng thử lại sau."
        )