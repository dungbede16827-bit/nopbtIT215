from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]


class Student(BaseModel):
    code: str
    name: str
    email: str
    age: int


@app.post("/students")
def create_student(student: Student):

    for s in students:
        if s["code"] == student.code:
            return {"message": "Code da ton tai"}

    if student.name == "":
        return {"message": "Name khong duoc rong"}

    if student.email == "":
        return {"message": "Email khong duoc rong"}

    if student.age <= 0:
        return {"message": "Age phai lon hon 0"}

    new_student = {
        "id": len(students) + 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)

    return {
        "message": "Them hoc vien thanh cong",
        "data": new_student
    }

@app.get("/students")
def get_students(keyword: str = "", min_age: int = 0, max_age: int = 100):

    result = []

    for s in students:
        if (
            keyword.lower() in s["name"].lower()
            or keyword.lower() in s["code"].lower()
            or keyword.lower() in s["email"].lower()
        ):
            if s["age"] >= min_age and s["age"] <= max_age:
                result.append(s)

    return {
        "message": "Danh sach hoc vien",
        "data": result
    }


@app.get("/students/{student_id}")
def get_student(student_id: int):

    for s in students:
        if s["id"] == student_id:
            return s

    return {"message": "Student not found"}


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):

    for s in students:
        if s["id"] == student_id:

            for item in students:
                if item["code"] == student.code and item["id"] != student_id:
                    return {"message": "Code da ton tai"}

            if student.name == "":
                return {"message": "Name khong duoc rong"}

            if student.email == "":
                return {"message": "Email khong duoc rong"}

            if student.age <= 0:
                return {"message": "Age phai lon hon 0"}

            s["code"] = student.code
            s["name"] = student.name
            s["email"] = student.email
            s["age"] = student.age

            return {
                "message": "Cap nhat thanh cong",
                "data": s
            }

    return {"message": "Student not found"}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for s in students:
        if s["id"] == student_id:
            students.remove(s)

            return {
                "message": "Xoa thanh cong",
                "data": s
            }

    return {"message": "Student not found"}