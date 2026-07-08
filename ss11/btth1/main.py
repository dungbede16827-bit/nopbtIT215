from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from database import engine, get_db
from models import Base, ParkingSlot
from schemas import ParkingSlotCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()


def response(
    status_code,
    message,
    error,
    data,
    path
):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/parking-slots", status_code=201)
def create_slot(
    slot: ParkingSlotCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    try:

        new_slot = ParkingSlot(
            slot_code=slot.slot_code,
            zone_name=slot.zone_name,
            max_weight=slot.max_weight,
            is_available=slot.is_available
        )

        db.add(new_slot)

        db.commit()

        db.refresh(new_slot)

        return response(
            201,
            "Thêm vị trí đỗ xe thành công",
            None,
            {
                "id": new_slot.id,
                "slot_code": new_slot.slot_code,
                "zone_name": new_slot.zone_name,
                "max_weight": new_slot.max_weight,
                "is_available": new_slot.is_available
            },
            request.url.path
        )

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="slot_code đã tồn tại"
        )

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Lỗi cơ sở dữ liệu"
        )


@app.get("/parking-slots")
def get_slots(
    request: Request,
    db: Session = Depends(get_db)
):

    slots = db.query(ParkingSlot).all()

    data = []

    for slot in slots:

        data.append({
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        })

    return response(
        200,
        "Lấy danh sách thành công",
        None,
        data,
        request.url.path
    )


@app.get("/parking-slots/{slot_id}")
def get_slot(
    slot_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    slot = db.query(ParkingSlot).filter(
        ParkingSlot.id == slot_id
    ).first()

    if slot is None:

        raise HTTPException(
            status_code=404,
            detail="Parking slot not found"
        )

    return response(
        200,
        "Lấy thông tin thành công",
        None,
        {
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        },
        request.url.path
    )