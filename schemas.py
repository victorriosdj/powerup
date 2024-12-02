from pydantic import BaseModel
from typing import List

from pydantic import BaseModel
from typing import List

class ProductoPedido(BaseModel):
    nombre: str
    precio: float

class Cliente(BaseModel):
    nombre: str
    direccion: str
    tarjeta: str
    fecha: str
    cvv: str

class Pedido(BaseModel):
    productos: List[ProductoPedido]
    total: float
    cliente: Cliente