from sqlalchemy import Column, Integer, String
from database import Base


class InventoryModel(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True)

    warehouse_code = Column(
        String(50),
        unique=True,
        nullable=False
    )

    location = Column(
        String(100),
        nullable=False
    )