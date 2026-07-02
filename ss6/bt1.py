from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

class Course(BaseModel):
    code: str
    name: str
    duration: int
    fee: int

@app.post("/courses")
def create_courses(course : Course) :
    
    for c in courses :
        if c["code"] == course.code :
            return {"message" : "Code đã tồn tại "}
        
    if course.name == "" :
        return {"message" : "tên không được rỗng"}
    
    if course.duration <= 0 :
        return {"message" : "Duration phai lon hon 0" } 
    
    if course.fee < 0:
        return {"message": "Fee phai lon hon hoac bang 0"}
    
    new_course = {
        "id": len(courses) + 1,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }

    course.append(new_course)

    return {
        "message" : "THÊM THÀNH CÔNG",
        "data" : new_course
    }


@app.get("/courses")
def get_courses(keyword: str = "", min_fee: int = 0, max_fee: int = 999999999):

    result = []

    for c in courses:
        if keyword.lower() in c["name"].lower() or keyword.lower() in c["code"].lower():
            if c["fee"] >= min_fee and c["fee"] <= max_fee:
                result.append(c)

    return {
        "message": "Danh sach khoa hoc",
        "data": result
    }

@app.get("/courses/{course_id}")
def get_course(course_id: int):

    for c in courses:
        if c["id"] == course_id:
            return c

    return {"message": "Course not found"}


@app.put("/courses/{course_id}")
def update_course(course_id: int, course: Course):

    for c in courses:
        if c["id"] == course_id:

            for item in courses:
                if item["code"] == course.code and item["id"] != course_id:
                    return {"message": "Code da ton tai"}

            if course.name == "":
                return {"message": "Name khong duoc rong"}

            if course.duration <= 0:
                return {"message": "Duration phai lon hon 0"}

            if course.fee < 0:
                return {"message": "Fee phai lon hon hoac bang 0"}

            c["code"] = course.code
            c["name"] = course.name
            c["duration"] = course.duration
            c["fee"] = course.fee

            return {
                "message": "Cap nhat thanh cong",
                "data": c
            }

    return {"message": "Course not found"}

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):

    for c in courses:
        if c["id"] == course_id:
            courses.remove(c)
            return {
                "message": "Xoa thanh cong",
                "data": c
            }

    return {"message": "Course not found"}