from fastapi import FastAPI
from routers import products, users
from fastapi.middleware.cors import CORSMiddleware 
from database import engine, Base
from models import products as models_products
from models import users as models_users


Base.metadata.create_all(bind=engine)

app = FastAPI(title = "API de Dietetica - Sistema de Gestion", description="""Esta es una  API REST construida con FastAPI
              ## Caracteristicas: 
              * **Autenticacion**: Sistema de Login con JWT (JSON Web Tokens)
              * **Base de Datos**: Uso de SQLite con SQLAlchemy (ORM) para manejar las tablas y relaciones de usuarios y productos
              * **Seguridad**: Hasheo de contraseñas y variables de entorno
              * **Escalabilidad**: Paginacion en consultas masivas.""",  version = "1.0.0",  contact={"name" : "Damaris Armoa", "url": "https://github.com/damarisarmoa12"})

origenes_permitidos = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origenes_permitidos, allow_credentials = True, allow_methods=["*"], allow_headers=["*"],)

app.include_router(products.router)
app.include_router(users.router)

