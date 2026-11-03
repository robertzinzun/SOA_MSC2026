from typing import List

from fastapi import APIRouter,Depends,HTTPException,status,Request
from fastapi.params import Query

from database.connection import Conexion
from database.eventDAO import EventoDAO
from database.connection import getConexion
eventsRouter=APIRouter(tags=["Eventos"])
from models.eventsModel import EventoInsert, EventoUpdate, Salida, Eventos, CupoEvento
from security.authenticate import authenticate_user, RoleChecker
from models.usersModel import Usuario
from main import limiter
#Definición de roles
roles=RoleChecker(["Organizador","Participante"])
organizador=RoleChecker(["Organizador"])

@eventsRouter.get("",summary="Consulta de Eventos",response_model=List[Eventos])
@limiter.limit("5/minute")
def consultaGeneralEventos(request:Request,offset:int=Query(default=0),limit:int=Query(default=10),cn:Conexion=Depends(getConexion),
                           user:Usuario=Depends(roles)):
    if user:
        edao=EventoDAO(cn)
        return edao.consultaGeneral(offset,limit)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado")

@eventsRouter.post("",response_model=Salida,summary="Agregar Evento")
@limiter.limit("5/minute")
def agregar(request:Request,evento:EventoInsert,cn:Conexion=Depends(getConexion),user:Usuario=Depends(organizador)):
    if user:
        edao = EventoDAO(cn)
        return edao.agregar(evento)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No autorizado")
@eventsRouter.get("/{id}",response_model=Eventos,summary="Consultar evento por ID")
@limiter.limit("5/minute")
def consultarEvento(request:Request,id:int,cn:Conexion=Depends(getConexion),user:Usuario=Depends(roles)):
    if user:
        edao = EventoDAO(cn)
        return edao.consultaPorId(id)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No autorizado")
@eventsRouter.put("/{id}",summary="Modificar Evento",response_model=Salida)
@limiter.limit("5/minute")
def modificarEvento(request:Request,id:int,evento:EventoUpdate,cn:Conexion=Depends(getConexion),user:Usuario=Depends(organizador)):
    if user:
        edao = EventoDAO(cn)
        return edao.modificar(id,evento)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
@eventsRouter.get('/tipoEvento/{idTipoEvento}',summary="Consultar eventos por Tipo",response_model=List[Eventos])
@limiter.limit("5/minute")
def consultaPorTipo(request:Request,idTipoEvento:int,cn:Conexion=Depends(getConexion),user:Usuario=Depends(roles)):
      if user:
        edao = EventoDAO(cn)
        return edao.consultaPorTipo(idTipoEvento)
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No autorizado")
@eventsRouter.get("/estatus/{estatus}",summary="Consultar eventos por estatus",response_model=List[Eventos])
@limiter.limit("5/minute")
def consultaPorEstatus(request:Request,estatus:str,cn:Conexion=Depends(getConexion),user:Usuario=Depends(roles)):
    if user:
        edao=EventoDAO(cn)
        return edao.consultaPorEstatus(estatus)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
@eventsRouter.get("/{idEvento}/cupo",summary="Consultar cupo de un evento",response_model=CupoEvento)
@limiter.limit("5/minute")
def validarCupo(request:Request,idEvento:int,cn:Conexion=Depends(getConexion),user:Usuario=Depends(roles)):
    if user:
        edao = EventoDAO(cn)
        return edao.validarCupo(idEvento)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
@eventsRouter.patch("/{idEvento}/{estatus}",summary="Cambiar estatus de un Evento",response_model=Salida)
@limiter.limit("5/minute")
def cambiarEstatus(request:Request,idEvento:int,estatus:str,cn:Conexion=Depends(getConexion),user:Usuario=Depends(organizador)):
    if user:
        edao = EventoDAO(cn)
        return edao.cambiarEstatus(idEvento,estatus)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
