# # khi gọi /getStudents 
# khi client gửi e cầu :
# Get / getstudents 

# tìm 
# @app.get("/getStudents")

# xong gọi hàm 
# def get_students():
#     return "Danh sach sinh vien: " + str(students)

# Giá trị trả về là:
# "Danh sach sinh vien: ['An', 'Binh', 'Cuong']"
# FastAPI gửi về cho client một chuỗi (string) thay vì một mảng JSON


# đây là một chuỗi văn bản 
# trong khi frontend đang đợi 

# [
#     "An",
#     "Binh",
#     "Cuong"
# ]
# Do đó Frontend không thể:

# duyệt danh sách bằng for
# hiển thị từng sinh viên
# xử lý dữ liệu như một mảng

# => API vẫn chạy nhưng không đúng định dạng dữ liệu mà Frontend yêu cầu

# nên dùng danh từ số nhiều /students 
# http dùng 
# GET / students 
# không cần ghi : /getStudents 

# sửa lại lỗi 



from fastapi import FastAPI

app = FastAPI()

students = ["An", "Binh", "Cuong"]


@app.get("/students")
def get_students():
    return students