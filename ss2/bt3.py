# API trả về một đối tượng JSON gồm
# message: Thông báo kết quả
# data: Danh sách sinh viên có trạng thái "active"

# Nếu có sinh viên đang học:

# {
#     "message": "Danh sách sinh viên đang học",
#     "data": [
#         {
#             "id": 1,
#             "name": "An",
#             "status": "active"
#         },
#         {
#             "id": 3,
#             "name": "Cuong",
#             "status": "active"
#         }
#     ]
# }

# Nếu không có sinh viên nào đang học:

# {
#     "message": "Không có sinh viên đang học",
#     "data": []
# }

# Điều kiện là:

# student["status"] == "active"

# Chỉ những sinh viên có status bằng "active" mới được đưa vào danh sách kết quả


from  fastapi import FastAPI

app = FastAPI()

students = [ {"id": 1, "name": "An", "status": "active"}, {"id": 2, "name": "Binh", "status": "inactive"}, {"id": 3, "name": "Cuong", "status": "active"}, {"id": 4, "name": "Dung", "status": "pending"} ]

@app.get("/students/active")
def get_active_students() :
    active_students = []

    for i in students :
        if i["status"] == "active" :
            active_students.append(i)

    if len(active_students) == 0 :
        return {
            "message": "Không có sinh viên đang học",
            "data": []
        }
    return { "message": "Danh sách sinh viên đang học", 
            "data": active_students 
            }
