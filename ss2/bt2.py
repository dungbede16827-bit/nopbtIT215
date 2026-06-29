# Endpoint hiện tại là:

# @app.get("/student")

# API này sử dụng phương thức GET với đường dẫn /student

# tester gọi GET/students 
# hai đường dẫn này khác nhau FastAPI chỉ xử lý những end point đã được khai báo . vì không tồn tại route students nên trả lỗi không có

# /student biểu thị một sinh viên.
# /students biểu thị danh sách nhiều sinh viên

# yc là lấy toàn bộ ds sinh viên nên đúng phải thêm s ở cuối

# Lệnh:

# return students[0]

# chỉ trả về phần tử đầu tiên trong danh sách.

# Kết quả nhận được:

# {
#     "id": 1,
#     "name": "An"
# }

# Trong khi yêu cầu của khách hàng là trả về toàn bộ danh sách sinh viên.

# Vì vậy cần trả về biến:

# return students

# để FastAPI tự chuyển thành JSON Array

# API đúng là:

# GET /students

# Đây là endpoint phù hợp với yêu cầu lấy danh sách tất cả sinh viên

# sửa lỗi 

from fastapi import FastAPI
app = FastAPI()

students = [ {"id": 1, "name": "An"}, {"id": 2, "name": "Binh"}, {"id": 3, "name": "Cuong"} ]

@app.get("/students")
def get_students() :
    return students
