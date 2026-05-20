from fastapi import APIRouter, HTTPException, Depends 
from sqlalchemy.orm import Session 
from schemas.products import Product, Id_Product, OrderCheckOut, PurchaseScheme
from models.products import ProductDB
from database import get_db
from routers.users import get_current_user
from models.users import UserDB

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/checkout", summary = "Procesar carrito de compras")
def process_cart(order : OrderCheckOut, db : Session = Depends(get_db)): 
    product_to_update = []

    for item in order.items:
        producto_db = db.query(ProductDB).filter(ProductDB.id == item.product_id).first()

        if not producto_db or producto_db.count < item.quantity_purchased: 
            raise HTTPException(status_code=400, detail=f"Falla de stock en el producto ID: {item.product_id}")
    
        producto_db.count -= item.quantity_purchased
        product_to_update.append(producto_db)

    db.commit()
    return {"mensaje" : "¡Compra exitosa!", "processed articles" : len(order.items)}


@router.post("/shopping", summary="Al comprar un producto bajara su stock")
def make_purchase(buy : PurchaseScheme,db : Session = Depends(get_db)): 
    product_db = db.query(ProductDB).filter(ProductDB.id == buy.product_id).first()

    if product_db.count < buy.quantity_purchased: 
        raise HTTPException(status_code=400, detail="No hay stock suficiente")
    
    product_db.count -= buy.quantity_purchased

    db.commit()
    return {"mensaje": "La compra ha sido exitosa"}

@router.get("/{id}", response_model=Id_Product)
async def get_product(id : int, db : Session = Depends(get_db)):
    producto = db.query(ProductDB).filter(ProductDB.id == id).first()

    if producto is None: 
        raise HTTPException(status_code = 404,  detail = "El producto no fue encontrado")
    return producto  
    
@router.get("/", response_model=list[Id_Product], summary="Obtener lista paginada de productos", description="Devuelve el inventario de la dietetica. Permite filtrar productos por un 'precio maximo' y cuenta con paginacion usando 'skip' y 'limit'.")
async def get_all_products(maximun_price : float | None = None, skip : int = 0, limit : int = 10,  db : Session = Depends(get_db)):
   query = db.query(ProductDB)

   if maximun_price is not None: 
       query = query.filter(ProductDB.price <= maximun_price)

   products = query.offset(skip).limit(limit).all()
   return products

@router.post("/", response_model=Id_Product, summary="Crea un producto nuevo (requiere token)", description="Crea un nuevo producto desde cero en el servidor.") 
async def post_products(product: Product, db : Session = Depends(get_db), current_user : UserDB = Depends(get_current_user)):
    new_product_db = ProductDB(**product.model_dump(), owner_id = current_user.id)

    if not current_user.is_admin: 
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")

    db.add(new_product_db)
    db.commit() 
    db.refresh(new_product_db)

    return new_product_db


@router.put("/{id}", response_model = Id_Product, summary="")
async def update_product(id : int, new_product : Product, current_user : UserDB = Depends(get_current_user), db : Session = Depends(get_db)):
    product_db = db.query(ProductDB).filter(ProductDB.id == id).first()

    if product_db is None: 
     raise HTTPException(status_code = 404, detail = "el producto que intentas actualizar no fue encontrado")
    
    if product_db.owner_id != current_user.id: 
        raise HTTPException(status_code=403, detail = "No tenes permiso para actualizar este producto")
    
    product_db.name = new_product.name
    product_db.price = new_product.price 
    product_db.count = new_product.count 
    
    db.commit()
    db.refresh(product_db)
    return product_db


@router.delete("/{id}", summary="Elimina un oroducto por su ID", description="Elimina un producto del inventario de la base de datos. Requiere autenticacion")
async def delete_product(id : int, current_user : UserDB = Depends(get_current_user), db : Session = Depends(get_db)): 
    product = db.query(ProductDB).filter(ProductDB.id == id).first()

    if product is None: 
        raise HTTPException(status_code=404,  detail ="El producto no fue encontrado")
    

    if product.owner_id != current_user.id: 
        raise HTTPException(status_code = 403, detail = "No tenes permiso para borrar este producto")
    
    db.delete(product)
    db.commit()

    return {"mensaje": f"El producto {product.name} fue eliminado exitosamente"}
    
