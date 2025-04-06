from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    tipo_usuario = Column(String(50))
    movimientos = relationship("Movimiento", back_populates="usuario")

class Movimiento(Base):
    __tablename__ = 'movimientos'
    id = Column(Integer, primary_key=True)
    tipo = Column(String(10))  # ingreso o egreso
    categoria = Column(String(50))
    monto = Column(Float)
    fecha = Column(Date, default=datetime.date.today)
    descripcion = Column(String(255))
    plazo = Column(String(20))  # diario, semanal, quincenal, mensual, anual
    metodo = Column(String(100))  # ejemplo: tarjeta Santander
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="movimientos")
