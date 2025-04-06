from db import get_session
from models import Movimiento

def agregar_movimiento(data):
    session = get_session()
    movimiento = Movimiento(**data)
    session.add(movimiento)
    session.commit()
    session.close()

def obtener_movimientos(usuario_id=None):
    session = get_session()
    query = session.query(Movimiento)
    if usuario_id is not None:
        query = query.filter(Movimiento.usuario_id == usuario_id)
    movimientos = query.all()
    session.close()
    return movimientos
