

from fastapi import HTTPException,status
from sqlmodel import select

from models.eventsModel import Eventos, EventoInsert, EventoUpdate, CupoEvento, Salida
from database.connection import Conexion

class EventoDAO:
   def __init__(self,conexion:Conexion):
      self.conexion=conexion
   def consultaGeneral(self,offset:int=0,limit:int=0):
      statement=select(Eventos).offset(offset).limit(limit)
      lista=self.conexion.get_session().exec(statement).all()
      self.conexion.cerrar()
      return lista
   def agregar(self,evento:EventoInsert):
      salida=Salida(estatus=False,mensaje="")
      try:
         self.conexion.get_session().add(evento)
         self.conexion.get_session().commit()
         self.conexion.cerrar()
         salida.estatus=True
         salida.mensaje=f"Evento creado con exito!!"
      except Exception as ex:
         print(f"Error:{ex}")
         salida.estatus=False
         salida.mensaje="Error al crear al evento, contacta al administrador."
      return salida
   def consultaPorId(self,id:int):
      evento=self.conexion.get_session().get(Eventos,id)
      if evento:
         return evento
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Evento no encontrado")

   def modificar(self,id:int,evento:EventoUpdate):
      salida=Salida(estatus=False,mensaje="")
      eventoFound=self.consultaPorId(id)
      if eventoFound and eventoFound.estatus not in['Finalizado','Cancelado']:
         eventoDATA=evento.model_dump(exclude_unset=True)
         eventoFound.sqlmodel_update(eventoDATA)
         self.conexion.get_session().commit()
         self.conexion.cerrar()
         salida.estatus=True
         salida.mensaje='Evento modificado con exito!!'
         return salida
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Evento con id:{id} no encontrado")
   def consultaPorTipo(self,tipo:int):
       #lista=self.conexion.get_session().query(Eventos).filter(Eventos.idTipoEvento==tipo).all()
       lista=self.conexion.get_session().exec(select(Eventos).where(Eventos.idTipoEvento==tipo)).all()
       self.conexion.get_session().close()
       return lista
   def consultaPorEstatus(self,estatus:str):
      estatusPermitidos=['Captura','Revision','Autorizado','Rechazado','En proceso','Cancelado','Suspendido','Finalizado']
      if estatus in estatusPermitidos:
         eventos=self.conexion.get_session().exec(select(Eventos).where(Eventos.estatus==estatus)).all()
         return eventos
      else:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estatus no encontrado")
   def validarCupo(self,idEvento:int):
      evento=self.conexion.get_session().get(CupoEvento,idEvento)
      if evento:
         return evento
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
   def cambiarEstatus(self, idEvento:int,estatus:str):
      TRANSICIONES = {
         "Captura": ["Revision"],
         "Revision": ["Autorizado", "Rechazado"],
         "Rechazado": ["Captura"],
         "Autorizado": ["En curso"],
         "En curso": ["Finalizado", "Suspendido"],
         "Suspendido": ["En curso", "Cancelado"],
         "Finalizado": [],
         "Cancelado": []
      }
      salida = Salida(estatus=False, mensaje="")
      try:
         evento=self.consultaPorId(idEvento)
         if evento:
            estatusActual=evento.estatus
            estatusValido=TRANSICIONES.get(estatusActual)
            if estatus in estatusValido:
               evento.estatus=estatus
               self.conexion.get_session().commit()
               salida.estatus=True
               salida.mensaje=f"El evento se cambio de {estatusActual} a {estatus}"
            else:
              salida.mensaje=f"El evento no se puede cambiar al estatus: {estatus}"
         else:
            salida.mensaje=f"El evento con id:{id} no existe."
      except Exception as ex:
         print(f"Error:{ex}")
         salida.mensaje="Error al cambiar el estatus, contacta al administrador."
      return salida






