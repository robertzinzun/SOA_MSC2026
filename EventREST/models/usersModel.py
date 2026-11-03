from sqlmodel import SQLModel,Field,AutoString
from pydantic import EmailStr,BaseModel
from enum import Enum
from typing import Optional
class Rol(Enum):
    Organizador='Organizador'
    Participante='Participante'
class Usuario(SQLModel,table=True):
    __tablename__ = 'Usuarios'
    idUsuario:int=Field(primary_key=True)
    nombre:str
    email:EmailStr=Field(unique=True,sa_type=AutoString)
    rol:Rol=Field(default=Rol.Participante)
    password:str
    estatus:bool
class UsuarioLogin(SQLModel):
    email:EmailStr
    password:str

class UsuarioSalida(BaseModel):
    estatus:bool
    mensaje:str
    usuario:Optional[Usuario]=None

class Token(BaseModel):
    access_token: str
    token_type: str
