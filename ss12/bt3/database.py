from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session


DATABASE_URL = "mysql+pymysql://root:123456d@localhost:3306/shipment_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False , autocommit=False,bind=engine)

Base = declarative_base()

class ShipmentModel(Base):
    __tablename_ = "shipments"

    id = Column(Integer,primary_key=True)
    tracking_code = Column(String(50),unique=True,nullable=False)
    receiver_name = Column(String(100),nullable=False)
    delivery_address = Column(String(255),nullable=False)


class ShipmentUpdate(BaseModel): 
    receiver_name : str
    delivery_address : str

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() :
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

def update_shipment_service(db:Session , shipment_id: int , shipment_update : ShipmentUpdate):
    shipment = (db.query(ShipmentModel).filter(ShipmentModel.id == shipment_id).first())
    if shipment is None :
        raise HTTPException(status_code=404,detail="KHÔNG TÌM THẤY ĐƠN GIAO HÀNG")
    
    shipment.receiver_name = shipment_update.receiver_name
    shipment.delivery_address = shipment_update.delivery_address

    db.commit()
    db.refresh(shipment)


@app.put("/shipments/{shipment_id}")
def update_shipment(shipment_id : int , shipment_update : ShipmentModel ,db: Session = Depends(get_db)):
    shipment = update_shipment_service(db,shipment_id,shipment_update)

    return {
        "message" : "Cập nhật đơn giao hàng thành công",
        "data" : shipment
    }
