from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey 
from database import Base 


class ProductDB(Base): 
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String, index = True)
    price = Column(Float)
    count = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id")) 
    