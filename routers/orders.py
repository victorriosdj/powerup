from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas, database

routerOrders = APIRouter()

@routerOrders.post("/guardarPedido", response_model=schemas.Pedido)
def guardar_pedido(pedido: schemas.Pedido, db: Session = Depends(database.get_db)):
    try:
        # Verificar si el cliente ya existe
        cliente = pedido.cliente
        cliente_existente = db.query(models.Cliente).filter(models.Cliente.nombre == cliente.nombre).first()

        # Si el cliente existe, usamos el cliente encontrado. Si no, creamos uno nuevo.
        if cliente_existente:
            cliente = cliente_existente
        else:
            # Si no existe el cliente, crear uno nuevo
            cliente = models.Cliente(
                nombre=cliente.nombre,
                direccion=cliente.direccion,
                tarjeta=cliente.tarjeta,
                fecha=cliente.fecha,
                cvv=cliente.cvv
            )
            db.add(cliente)
            db.commit()  # Guardamos el nuevo cliente
            db.refresh(cliente)  # Refrescamos para obtener el ID del cliente recién creado

        # Crear el pedido asociado al cliente
        nuevo_pedido = models.Pedido(
            cliente_id=cliente.id,  # Relacionamos el pedido con el cliente mediante cliente_id
            total=pedido.total  # Asegúrate de que total sea calculado correctamente antes de guardar
        )
        db.add(nuevo_pedido)
        db.commit()  # Guardamos el pedido
        db.refresh(nuevo_pedido)  # Refrescamos para obtener el ID del nuevo pedido

        # Crear los productos del pedido
        for producto in pedido.productos:
            producto_pedido = models.ProductoPedido(
                pedido_id=nuevo_pedido.id,  # Asociamos el producto con el pedido
                nombre=producto.nombre,
                precio=producto.precio
            )
            db.add(producto_pedido)

        db.commit()  # Guardamos todos los productos

        # Devolvemos el nuevo pedido con los datos relacionados
        return nuevo_pedido
    except Exception as e:
        # Manejo de errores y rollback en caso de falla
        db.rollback()
        return {"error": "Error al guardar el pedido", "details": str(e)}

