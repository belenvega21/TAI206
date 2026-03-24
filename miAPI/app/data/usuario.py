from sqlalchemy import Column, Integer, String
from app.data.db import base

class Usuario(base):
    __tablename__ = "tb_usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)