# API Dietética - Gestión de Inventario

Primer proyecto integral de Backend. Es una API REST construida desde cero con FastAPI para manejar el stock y los usuarios de una dietetica. 

# Tecnologias 

* **Python** 
* **FastAPI**
* **SQLAlchemy** 
* **Pydantic**
* **PyJWT & Bcrypt**

# ¿Que me enfoque en resolver? 

* **Seguridad:** Las contraseñas de los usuarios no se guardan legibles. Se hashean con Bcrypt apenas entran al sistema.
* **Autenticacion:** Implemente JSON Web Tokens (JWT). Si un usuario no esta logueado o su token expiró. la API da un error 401
* **Reglas de negocio:** Delegué la responsabilidad a la base de datos para que sea imposible registrar dos mails iguales, y armé la lógica para que solo el creador original de un producto pueda editarlo o borrarlo.
* **Ciclo de vida de los datos:** Use inyección de dependencia y generadores ('yield') para abrir y cerrar las conexiones a la base de datos en cada petición, evitando memory leaks.
* **Proceso de las compras:** Procesa un carrito de compras completo. Recibe una lista de productos y cantidades, valida que exista stock suficiente para todos los items y descuenta el stock de forma segura.


