from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, InventoryModel
from schemas import InventoryCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post(
    "/inventories",
    status_code=status.HTTP_201_CREATED
)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):

    old_inventory = db.query(InventoryModel).filter(
        InventoryModel.warehouse_code == inventory.warehouse_code
    ).first()

    if old_inventory:
        raise HTTPException(
            status_code=400,
            detail="Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng"
        )

    new_inventory = InventoryModel(
        warehouse_code=inventory.warehouse_code,
        location=inventory.location
    )

    db.add(new_inventory)

    db.commit()

    db.refresh(new_inventory)

    return {
        "message": "Tạo kho vận thành công"
    }