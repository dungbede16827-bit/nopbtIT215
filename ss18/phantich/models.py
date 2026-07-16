from sqlalchemy import Column,Integer,String,ForeignKey
from database import Base

class Student(Base):
    __tablename__="students"

    id=Column(Integer,primary_key=True)
    full_name=Column(String(255))
    email=Column(String(255))
    status=Column(String(50))


class Course(Base):
    __tablename__="courses"

    id=Column(Integer,primary_key=True)
    name=Column(String(255))
    status=Column(String(50))


class Enrollment(Base):
    __tablename__="enrollments"

    id=Column(Integer,primary_key=True)
    student_id=Column(Integer,ForeignKey("students.id"))
    course_id=Column(Integer,ForeignKey("courses.id"))
    status=Column(String(50))