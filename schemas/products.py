from pydantic import BaseModel, Field 

class Product(BaseModel): 
    name: str
    price: float = Field(gt=0, description="El precio debe ser estrictamente mayor que 0")
    count: int = Field(ge=0)

# Lo que nosotros devolveremos 
class Id_Product(Product): 
    id: int
    model_config = {"from_attributes" : True}