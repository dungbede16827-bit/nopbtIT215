# # Input
# # Danh sách các khóa học được lưu trong một list Python.
# # course_id được truyền qua Path Parameter khi xem chi tiết khóa học.

# # Output
# # API 1

# # GET /health

# # {
# #     "message": "API is running"
# # }
# # API 2

# # GET /courses

# # Trả về toàn bộ danh sách khóa học
# # API 3

# # GET /courses/{course_id}

# # Nếu tìm thấy khóa học → trả về thông tin khóa hc
# # Nếu không tìm thấy → trả về lỗi 404
# # Nếu course_id <= 0 → trả về lỗi 400
# Thiết kế luồng xử lý
# API 1: GET /health
# Khởi tạo FastAPI
# Tạo endpoint /health
# Trả về thông báo API đang hoạt động
# API 2: GET /courses
# Tạo endpoint /courses
# Trả về toàn bộ danh sách courses
# API 3: GET /courses/{course_id}
# Nhận course_id
# Kiểm tra:
# Nếu course_id <= 0 → báo lỗi 400
# Duyệt danh sách courses
# Nếu tìm thấy khóa học:
# Trả về dữ liệu khóa học
# Nếu duyệt hết mà không tìm thấy:
# Trả về lỗi 404

from fastapi import FastAPI, HTTPException

app = FastAPI()

courses = [
    {
        "id": 1,
        "code": "PY101",
        "name": "Python Basic",
        "level": "beginner",
        "price": 1500000
    },
    {
        "id": 2,
        "code": "FA101",
        "name": "FastAPI Basic",
        "level": "beginner",
        "price": 2000000
    },
]

@app.get("/courses") 
def get_courses() :
    return {
        "message": "API is running"
    }

@app.get("/courses/{course_id}")
def get_course(course_id: int):

    if course_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="course_id phải lớn hơn 0"
        )

    for course in courses:
        if course["id"] == course_id:
            return course

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy khóa học"
    )