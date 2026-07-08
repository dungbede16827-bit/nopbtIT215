from pydantic import BaseModel


class InventoryCreate(BaseModel):
    warehouse_code: str
    location: str