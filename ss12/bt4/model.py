# Tìm học viên theo student_id.
# Nếu không tồn tại → báo lỗi 404.
# Nếu tồn tại:
# Lưu lại thông tin học viên.
# Gọi db.delete(student).
# Gọi db.commit().
# Trả về thông tin học viên đã xóa.

# Ưu điểm

# Dễ hiểu.
# Kiểm soát lỗi tốt.
# Đúng quy trình của SQLAlchemy ORM.
# Phù hợp mô hình Service.
# Giải pháp 2

# Thực hiện câu lệnh Delete trực tiếp:

# db.query(StudentModel).filter(StudentModel.id == student_id).delete()
# db.commit()

# Ưu điểm

# Code ngắn.
# Thực hiện nhanh.

# Nhược điểm

# Không lấy được thông tin học viên trước khi xóa.
# Khó trả về dữ liệu đã xóa.
# Khó kiểm tra học viên có tồn tại hay không.

from sqlalchemy import Column, Integer, String
from database import Base

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)