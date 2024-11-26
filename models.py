# Importamos las dependencias necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime  # Columnas para la base de datos y tipos de datos
from sqlalchemy.orm import relationship  # Para crear relaciones entre tablas
from database import Base  # Importamos la clase base de SQLAlchemy para definir las tablas
from datetime import datetime  # Para trabajar con fechas y horas

# Modelo de la tabla "productos"
class Productos(Base):
    # Definimos el nombre de la tabla en la base de datos
    __tablename__ = 'productos'
    
    # Definición de la columna "id_producto" que es la clave primaria
    id_producto = Column(Integer, primary_key=True)
    
    # Definición de la columna "nom_prod" que almacena el nombre del producto (máximo 100 caracteres)
    nom_prod = Column(String(100), nullable=False)
    
    # Definición de la columna "catg_prod" que almacena la categoría del producto (máximo 50 caracteres)
    # La columna es única, lo que significa que no puede haber dos productos con la misma categoría
    catg_prod = Column(String(50), nullable=False, unique=True)
    
    # Definición de la columna "precio_prod" que almacena el precio del producto (en formato entero)
    # Esta columna también es única, lo que significa que no puede haber dos productos con el mismo precio
    precio_prod = Column(Integer, nullable=False, unique=True)
