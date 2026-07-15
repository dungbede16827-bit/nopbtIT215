# Giải pháp 1 (secondary)

# Dùng secondary để nối trực tiếp Student và Course.

# Có thể gọi

# course.students

# hoặc

# student.courses

# Không cần đi qua Enrollment.

# Ưu điểm

# Code ngắn
# Dễ dùng
# Truy vấn nhanh
# Giải pháp 2

# Không dùng secondary.

# Quan hệ sẽ là

# Student
#      |
#      |
# Enrollment
#      |
#      |
# Course

# Muốn lấy sinh viên

# for enrollment in course.enrollments:
#     print(enrollment.student)

# Phải đi qua Enrollment.

# Code dài hơn.

# 6.3 So sánh
# Tiêu chí	Giải pháp 1 (secondary)	Giải pháp 2 (2 quan hệ 1-N)
# Code	Ngắn gọn	Dài hơn
# Truy xuất	course.students	Phải dùng vòng lặp
# Dễ hiểu	Dễ	Khó hơn

# chọn Giải pháp 1.

# Lý do:

# Code ngắn.
# Dễ đọc.
# Dễ truy xuất dữ liệu.
# Có thể lấy danh sách sinh viên bằng course.students.
# Phù hợp với cách học trong slide SQLAlchemy.
# 6.5 Các bước thiết kế
# Tạo Base.
# Tạo class Student.
# Tạo class Course.
# Tạo class Enrollment.
# Khai báo Primary Key.
# Khai báo ForeignKey.
# Khai báo relationship().
# Thêm back_populates.
# Kiểm tra các quan hệ đã liên kết đúng.


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    email = Column(String(100))
    enrollments = relationship("Enrollment",back_populates="student")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    enrollments = relationship("Enrollment",back_populates="course")


class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer,ForeignKey("students.id"))
    course_id = Column(Integer,ForeignKey("courses.id"))
    student = relationship("Student",back_populates="enrollments")
    course = relationship("Course",back_populates="enrollments")
