from sqlmodel import SQLModel,Field,Enum
from datetime import date
from typing import Optional
from pydantic import BaseModel, model_validator, ValidationError


class EventoBase(SQLModel):
    nombre: str = Field(unique=True)
    descripcion: Optional[str] = Field(default=None)
    fechaRegistro: Optional[date] = Field(default=None)
    fechaInicio: Optional[date] = Field(default=None)
    fechaFin: Optional[date] = Field(default=None)
    capacidad: Optional[int] = Field(None, gt=0)
    inscritos: int = Field(default=None)
    costoEvento: float = Field(default=None)
    cuotaRecuperacion: float = Field(default=None)
    idTipoEvento:int
    modalidad: str = Field(default='Presencial')

    @model_validator(mode='after')
    def validarFechas(self):
        if self.fechaInicio>self.fechaFin:
            raise ValueError('Periodo de fechas Invalido')
        return self
class EventoUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None)
    descripcion: Optional[str] = Field(default=None)
    fechaRegistro: Optional[date] = Field(default=None)
    fechaInicio: Optional[date] = Field(default=None)
    fechaFin: Optional[date] = Field(default=None)
    capacidad: Optional[int] = Field(None, gt=0)
    inscritos: Optional[int] = Field(default=None)
    costoEvento: Optional[float] = Field(default=None)
    cuotaRecuperacion: Optional[float] = Field(default=None)
    estatus: Optional[str] = Field(default=None)
    modalidad: Optional[str] = Field(default=None)
    idTipoEvento: Optional[int]=Field(default=None)
class EventoInsert(EventoBase,table=True):
    __tablename__ = 'Eventos'
    idEvento:Optional[int]=Field(primary_key=True)

class Eventos(EventoBase,table=True):
    __tablename__ = "vEventos"
    idEvento: Optional[int] = Field(primary_key=True)
    estatus:str
    tipo:str
class CupoEvento(SQLModel,table=True):
    __tablename__ = "CupoEvento"
    idEvento:int=Field(primary_key=True)
    nombre:str
    capacidad:int
    inscritos:int
    cupo:int
    disponible:bool

class Salida(SQLModel):
    estatus:bool
    mensaje:str

