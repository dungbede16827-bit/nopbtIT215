# Input của bài toán

# Danh sách books:

# books = [
#     {"id": 1, "title": "Python Basic", "quantity": 12},
#     {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
#     {"id": 3, "title": "Clean Code", "quantity": 5},
#     {"id": 4, "title": "Database Design", "quantity": 0},
#     {"id": 5, "title": "Web API Design", "quantity": 20}
# ]

# Output mong muốn

# API trả về danh sách các sách có số lượng tồn kho nhỏ hơn hoặc bằng 5

# Nếu có dữ liệu:

# {
#     "message": "Danh sách sách sắp hết hàng",
#     "data": [
#         {
#             "id": 2,
#             "title": "FastAPI Beginner",
#             "quantity": 3
#         },
#         {
#             "id": 3,
#             "title": "Clean Code",
#             "quantity": 5
#         },
#         {
#             "id": 4,
#             "title": "Database Design",
#             "quantity": 0
#         }
#     ]
# }

# Nếu không có dữ liệu:

# {
#     "message": "Không có sách nào sắp hết hàng",
#     "data": []
# }

# Điều kiện xác định sách sắp hết hàng
# Có trường quantity.
# quantity >= 0
# quantity <= 5

# Nếu:

# thiếu trường quantity → bỏ qua
# quantity < 0 → bỏ qua


# giải pháp dùng vòng lặp for

# Tạo danh sách rỗng low_stock
# Duyệt từng quyển sách
# Kiểm tra có trường quantity hay không
# Kiểm tra quantity có hợp lệ hay không
# Nếu quantity <= 5 thì thêm vào danh sách


# Khởi tạo ứng dụng FastAPI
# Khai báo danh sách books
# Tạo endpoint
# GET /books/low-stock
# Tạo danh sách rỗng low_stock
# Duyệt từng quyển sách
# Nếu thiếu trường quantity thì bỏ qua
# Nếu quantity < 0 thì bỏ qua
# Nếu quantity <= 5 thì thêm vào danh sách
# Nếu danh sách rỗng thì trả về:

from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20},
    {"id": 6, "title": "Java Basic"},
    {"id": 7, "title": "Spring Boot", "quantity": -2}
]

@app.get("/books/low-stock")
def get_low_stock_books() :
    low_stock = []
    
    for i in books :
        if "quantity" not in books :
            continue

        quantity = i["quantity"]

        if quantity < 0 :
            continue

        if quantity <= 5:
            low_stock.append(i)
        
        if len(low_stock) == 0:
            return {
                "message": "Không có sách nào sắp hết hàng",
                "data": []
            }
        
        return {
        "message": "Danh sách sách sắp hết hàng",
        "data": low_stock
    }

        
