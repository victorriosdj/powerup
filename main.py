# Importamos las dependencias necesarias
from fastapi import FastAPI, Request  # FastAPI para crear la aplicación y Request para manejar peticiones
from routers.products import getProductsRouter  # Importamos las rutas del módulo de productos
from fastapi.templating import Jinja2Templates  # Para trabajar con plantillas HTML mediante Jinja2
from fastapi.staticfiles import StaticFiles  # Para servir archivos estáticos como CSS, JS, imágenes
from dotenv import load_dotenv  # Para cargar variables de entorno desde un archivo .env

# Crear la instancia de la aplicación FastAPI
app = FastAPI()

# Configuración de Jinja2 para trabajar con templates HTML en la carpeta "templates"
templates = Jinja2Templates(directory="templates")

# Ruta principal
@app.get("/")
async def root(request: Request):
    # Retorna la respuesta con el template "index.html"
    # Se pasa el objeto "request" para que Jinja2 pueda acceder a la información de la solicitud
    return templates.TemplateResponse("index.html", {"request": request})

# Incluir las rutas definidas en el router de productos
app.include_router(getProductsRouter)

# Rutas estáticas: Monta la carpeta "static" en la URL "/static"
# Los archivos en la carpeta "static" se pueden servir directamente (como CSS, JS, imágenes, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cargar variables de entorno desde un archivo .env
load_dotenv()

@app.get("/tienda")
async def tienda(request: Request):
    # Retorna la respuesta con el template "productos.html"
    return templates.TemplateResponse("productos.html", {"request": request})

@app.get("/pago")
async def pago(request: Request):
    return templates.TemplateResponse("pago.html", {"request": request})







