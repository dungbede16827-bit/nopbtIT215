from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from model import StudentModel

app = FastAPI()

StudentModel.metadata.create_all(bind=engine)

# Kết nối database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def delete_student_service(db: Session, student_id: int):

    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Học viên không tồn tại trong hệ thống"
        )

    result = {
        "id": student.id,
        "full_name": student.full_name,
        "email": student.email
    }

    db.delete(student)
    db.commit()

    return result


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = delete_student_service(db, student_id)

    return {
        "message": "Xóa học viên thành công",
        "data": student
    }