from fastapi import HTTPException
from models import Student, Course, Enrollment

def get_students_by_course(course_id, db):

    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    students = (
        db.query(Student)
        .join(
            Enrollment,
            Student.id == Enrollment.student_id
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.status.in_(["STUDYING", "COMPLETED"]),
            Student.status == "ACTIVE"
        )
        .distinct()
        .order_by(Student.full_name)
        .all()
    )

    result = []

    for student in students:
        result.append({
            "id": student.id,
            "full_name": student.full_name,
            "email": student.email
        })

    return {
        "course_id": course.id,
        "course_name": course.name,
        "total_students": len(result),
        "students": result
    }