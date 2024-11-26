# Importamos las dependencias necesarias
from fastapi import Depends, Request, APIRouter, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Productos
from fastapi.templating import Jinja2Templates

# Configuración de Jinja2 para trabajar con templates HTML en la carpeta "templates"
templates = Jinja2Templates(directory="templates")

# Dependencia para obtener la sesión de base de datos
def get_db():
    # Abrir una nueva sesión de base de datos
    db = SessionLocal()
    try:
        yield db  # Retornar la sesión de base de datos
    finally:
        db.close()  # Cerrar la sesión de base de datos cuando termine

# Definición del router que maneja las rutas de productos
getProductsRouter = APIRouter(
    tags=["getProducts"],  # Etiqueta para la ruta
    responses={404: {"message": "No encontrado"}}  # Respuesta en caso de error 404
)

# Ruta para renderizar la tabla de productos en el template HTML
@getProductsRouter.get("/templateProductsTable")
async def templateUsersTable(request: Request, db: Session = Depends(get_db)):
    # Consultar todos los productos en la base de datos
    productos = db.query(Productos.id_producto, Productos.nom_prod, Productos.catg_prod, Productos.precio_prod).all()
    
    # Retornar la respuesta con el template HTML y los productos obtenidos
    return templates.TemplateResponse("ingresar_prod.html", {
        "request": request,  # Necesario para que Jinja2 funcione
        "productos": productos,  # Pasar la lista de productos al template
        "active_page": request.url.path  # Ruta actual activa
    })

# Ruta para registrar un nuevo producto en la base de datos
@getProductsRouter.post("/register_product")
async def register_product(
    request: Request,
    nom_prod: str = Form(...),  # El nombre del producto que se recibe desde el formulario
    catg_prod: str = Form(...),  # La categoría del producto
    precio_prod: int = Form(...),  # El precio del producto (en entero, si es un valor entero)
    db: Session = Depends(get_db)  # Dependencia para obtener la sesión de la base de datos
):
    # Verificar si el producto ya existe en la base de datos
    producto = db.query(Productos).filter(Productos.nom_prod == nom_prod).first()

    if producto:  # Si el producto ya existe
        # Retornar al template con un mensaje de error
        return templates.TemplateResponse("ingresar_prod.html", {"request": request, "error": "El producto ya existe"})
    
    # Crear un nuevo objeto de Producto
    nuevo_producto = Productos(
        nom_prod=nom_prod,  # Asignar el nombre del producto
        catg_prod=catg_prod,  # Asignar la categoría
        precio_prod=precio_prod  # Asignar el precio
    )

    # Añadir el nuevo producto a la sesión de base de datos
    db.add(nuevo_producto)
    # Confirmar los cambios en la base de datos
    db.commit()
    # Refrescar el objeto para obtener la información actualizada del producto
    db.refresh(nuevo_producto)

    # Redirigir a la página con la tabla de productos
    return RedirectResponse(url="/templateProductsTable", status_code=303)

# Ruta para eliminar un producto de la base de datos
@getProductsRouter.delete("/deleteProduct")
async def delete_product(
    id_producto: int,  # El ID del producto que se desea eliminar
    db: Session = Depends(get_db)  # Obtener la sesión de base de datos
):
    # Buscar el producto por su ID
    producto = db.query(Productos).filter(Productos.id_producto == id_producto).first()
    
    # Si el producto existe
    if producto:
        # Eliminar el producto de la base de datos
        db.query(Productos).filter(Productos.id_producto == id_producto).delete()

    # Confirmar los cambios en la base de datos
    db.commit()

    # Redirigir a la página con la tabla de productos
    return RedirectResponse(url="/templateProductsTable", status_code=303)

# Ruta para editar un producto existente
@getProductsRouter.post("/editProduct")
async def editProduct(
    id_producto: int,  # El ID del producto que se desea editar
    nom_prod: str = Form(...),  # El nuevo nombre del producto
    catg_prod: str = Form(...),  # La nueva categoría del producto
    precio_prod: float = Form(...),  # El nuevo precio del producto (como float por si hay decimales)
    db: Session = Depends(get_db)  # Obtener la sesión de base de datos
):
    # Buscar el producto por su ID
    producto = db.query(Productos).filter(Productos.id_producto == id_producto).first()

    if producto:  # Si el producto existe
        # Actualizar el producto con los nuevos valores
        db.query(Productos).filter(Productos.id_producto == id_producto).update({
            Productos.nom_prod: nom_prod,
            Productos.catg_prod: catg_prod,
            Productos.precio_prod: precio_prod
        })
        # Confirmar los cambios en la base de datos
        db.commit()

    # Redirigir a la página con la tabla de productos
    return RedirectResponse(url="/templateProductsTable", status_code=303)
