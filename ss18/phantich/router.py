from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from service import get_students_by_course

router = APIRouter()

@router.get("/courses/{course_id}/students")
def course_students(
    course_id: int,
    db: Session = Depends(get_db)
):
    return get_students_by_course(course_id, db)