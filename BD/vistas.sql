-- Creacion de vistas
create view vEventos
as
select idEvento,e.nombre,e.descripcion,fechaRegistro,
fechaInicio,fechaFin,capacidad,inscritos,costoEvento,
cuotaRecuperacion,estatus,modalidad,idDepartamento,
e.idTipoEvento,t.nombre tipo from Eventos e
join TipoEvento t using(idTipoEvento);

create view CupoEvento
as
select idEvento,nombre,capacidad,inscritos,
capacidad-inscritos as cupo,
case 
when capacidad-inscritos>0 then true
else false
end as disponible
from Eventos;

create view EtapaEvento
as
select et.idEtapa,ev.nombre evento,ev.idEvento,et.idTipoEtapa, t.nombre etapa,et.fechaInicio,et.fechaFin,
et.estatus,et.observaciones,et.idDepartamento
from Etapas et join Eventos ev using(idEvento)
join TipoEtapa t using(idTipoEtapa);

create view vActividades
as
select idActividad,a.nombre actividad,a.fechaInicio,a.fechaFin,
a.estatus,a.descripcion,e.idEvento,e.nombre evento,a.idEtapa,
et.etapa
from Actividades a join Eventos e using(idEvento)
join EtapaEvento et using(idEtapa);
