
from fastapi import APIRouter, HTTPException, Depends 
from sqlalchemy.orm import Session 
from schemas.users import User, Id_user 
from models.users import UserDB 
from database import get_db 
from security import get_password_hash, verify_password, create_access_token
import jwt
from jwt.exceptions import InvalidTokenError
from security import SECRET_KEY, ALGORITHM, oauth2_scheme


router = APIRouter(prefix = "/users", tags = ["Users"])

async def get_current_user(token: str= Depends(oauth2_scheme), db : Session = Depends(get_db)): 
    credencials_exception = HTTPException(status_code=401, detail = "No se pudieron validar las credenciales", headers={"WWW-Authenticate" : "Bearer"})

    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        email: str = payload.get("sub")
        if email is None: 
            raise credencials_exception
    
    except InvalidTokenError: 
        raise credencials_exception
    
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if user is None: 
        raise credencials_exception
    
    return user 
    

@router.get("/me", response_model=Id_user)
async def read_users_me(current_user : UserDB = Depends(get_current_user)): 
    return current_user

@router.get("/{id}", response_model=Id_user)
async def get_product(id : int, db : Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == id).first() 

    if user is None: 
        raise HTTPException(status_code = 404,  detail = "El producto no fue encontrado")
    return user 

@router.post("/",  response_model = Id_user)
async def create_user(user : User, db : Session = Depends(get_db)): 
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user: 
        raise HTTPException(status_code = 400, detail="El email ya esta registrado")
    
    hashed_pw = get_password_hash(user.password) 

    new_user = UserDB(email=user.email, hashed_password = hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user 

@router.post("/login")
async def login_for_access_token(user_credential: User, db: Session = Depends(get_db)): 
    user = db.query(UserDB).filter(UserDB.email == user_credential.email).first()

    if not user or not verify_password(user_credential.password, user.hashed_password): 
        raise HTTPException(status_code = 401, detail = "Email o contraseña incorrecta")
    
    access_token = create_access_token(data={"sub" : user.email})
    return {"access_token": access_token, "token_type": "bearer"}




