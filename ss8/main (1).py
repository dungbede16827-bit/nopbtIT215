from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

carriers = [
    {"id":1,"code":"GHN","name":"Giao Hang Nhanh","max_weight_capacity":5000,"status":"ACTIVE"},
    {"id":2,"code":"GHTK","name":"Giao Hang Tiet Kiem","max_weight_capacity":3000,"status":"ACTIVE"},
    {"id":3,"code":"VTP","name":"Viettel Post","max_weight_capacity":10000,"status":"SUSPENDED"},
]

shipments = [
    {"id":1,"carrier_id":1,"order_reference":"ORD-2026-001","total_weight":4200,"dispatch_date":"2026-07-01","shift":"MORNING"}
]

class Carrier(BaseModel):
    code:str
    name:str
    max_weight_capacity:int
    status:str

class Shipment(BaseModel):
    carrier_id:int
    order_reference:str
    total_weight:int
    dispatch_date:str
    shift:str

@app.post("/carriers",status_code=status.HTTP_201_CREATED)
def create_carrier(carrier:Carrier):
    if carrier.name.strip()=="":
        raise HTTPException(status_code=400,detail="Tên đối tác không được để trống")
    if len(carrier.name)<3:
        raise HTTPException(status_code=400,detail="Tên đối tác phải có ít nhất 3 ký tự")
    if carrier.max_weight_capacity<=0:
        raise HTTPException(status_code=400,detail="Tải trọng tối đa phải lớn hơn 0")
    if carrier.status not in ["ACTIVE","INACTIVE","SUSPENDED"]:
        raise HTTPException(status_code=400,detail="Trạng thái không hợp lệ")
    for c in carriers:
        if c["code"].lower()==carrier.code.lower():
            raise HTTPException(status_code=400,detail="Mã đối tác vận chuyển đã tồn tại")
    new=carrier.model_dump()
    new["id"]=len(carriers)+1
    carriers.append(new)
    return new

@app.get("/carriers")
def get_carriers(keyword:str=None,status:str=None,min_weight:int=None):
    result=[]
    for c in carriers:
        if keyword:
            if keyword.lower() not in c["code"].lower() and keyword.lower() not in c["name"].lower():
                continue
        if status:
            if c["status"]!=status:
                continue
        if min_weight:
            if c["max_weight_capacity"]<min_weight:
                continue
        result.append(c)
    return result

@app.get("/carriers/{carrier_id}")
def get_carrier(carrier_id:int):
    for c in carriers:
        if c["id"]==carrier_id:
            return c
    raise HTTPException(status_code=404,detail="Không tìm thấy đối tác vận chuyển")

@app.put("/carriers/{carrier_id}")
def update_carrier(carrier_id:int,carrier:Carrier):
    if carrier.name.strip()=="" or len(carrier.name)<3:
        raise HTTPException(status_code=400,detail="Tên đối tác không hợp lệ")
    if carrier.max_weight_capacity<=0:
        raise HTTPException(status_code=400,detail="Tải trọng tối đa phải lớn hơn 0")
    if carrier.status not in ["ACTIVE","INACTIVE","SUSPENDED"]:
        raise HTTPException(status_code=400,detail= "Trạng thái không hợp lệ")
    for c in carriers:
        if c["id"]!=carrier_id and c["code"].lower()==carrier.code.lower():
            raise HTTPException(status_code=400,detail="Mã đối tác vận chuyển đã tồn tại")
    for i in range(len(carriers)):
        if carriers[i]["id"]==carrier_id:
            data=carrier.model_dump()
            data["id"]=carrier_id
            carriers[i]=data
            return data
    raise HTTPException(status_code=404,detail="Không tìm thấy đối tác vận chuyển")

@app.delete("/carriers")
def delete_carrier(carrier_id:int):
    for i in range(len(carriers)):
        if carriers[i]["id"]==carrier_id:
            del carriers[i]
            return {"message":"Xóa thành công"}
    raise HTTPException(status_code=404,detail="Không tìm thấy đối tác vận chuyển")

@app.post("/shipments",status_code=status.HTTP_201_CREATED)
def create_shipment(shipment:Shipment):
    if shipment.total_weight<=0:
        raise HTTPException(status_code=400,detail="Khối lượng chuyến hàng phải lớn hơn 0")
    if shipment.shift not in ["MORNING","AFTERNOON","NIGHT"]:
        raise HTTPException(status_code=400,detail="Ca làm việc không hợp lệ")
    carrier=None
    for c in carriers:
        if c["id"]==shipment.carrier_id:
            carrier=c
    if carrier is None:
        raise HTTPException(status_code=404,detail="Không tìm thấy đối tác vận chuyển")
    if carrier["status"]!="ACTIVE":
        raise HTTPException(status_code=400,detail="Đối tác vận chuyển không hoạt động")
    if shipment.total_weight>carrier["max_weight_capacity"]:
        raise HTTPException(status_code=400,detail="Khối lượng vượt quá tải trọng tối đa")
    for s in shipments:
        if s["carrier_id"]==shipment.carrier_id and s["dispatch_date"]==shipment.dispatch_date and s["shift"]==shipment.shift:
            raise HTTPException(status_code=400,detail="Đối tác đã có chuyến hàng trong cùng ngày và ca")
    data=shipment.model_dump()
    data["id"]=len(shipments)+1
    shipments.append(data)
    return data

@app.get("/shipments")
def get_shipments():
    return shipments
