from pydantic import BaseModel, Field, EmailStr

class User(BaseModel): 
    email : EmailStr
    password  : str = Field(max_length=72)


class Id_user(BaseModel):  
    id : int 
    email : str 

    model_config = {"from_attributes" : True}



