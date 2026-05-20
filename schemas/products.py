from pydantic import BaseModel, Field 

class Product(BaseModel): 
    name: str
    price: float = Field(gt=0, description="El precio debe ser estrictamente mayor que 0")
    count: int = Field(ge=0)

class Id_Product(Product): 
    id: int
    model_config = {"from_attributes" : True}

class PurchaseScheme(BaseModel): 
    product_id : int 
    quantity_purchased : int 

class OrderCheckOut(BaseModel): 
    items: list[PurchaseScheme] 
    payment_method : str 