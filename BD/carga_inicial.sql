INSERT INTO TipoEvento ( nombre, descripcion) VALUES
( 'PLATICA INFORMATIVA','Plática informativa de procesos académicos'),
( 'CONCURSO','Concurso de habilidades académicas'),
( 'CONFERENCIA','Conferencia académica'),
( 'REUNION','Reunión académica o administrativa'),
( 'TALLER','Taller práctico'),
( 'SEMINARIO','Seminario académico'),
( 'JORNADA','Jornada académica'),
( 'DEFENSA DE PROYECTO','Defensa de proyecto de fin de carrera/posgrado'),
( 'PRACTICA','Prácticas en laboratorio'),
( 'MANTENIMIENTO','Mantenimiento preventivo/correcctivo de instalaciones');
select * from TipoEvento;
INSERT INTO TipoEtapa (nombre, descripcion, orden) VALUES
('PLANEACIÓN',   'Definición y organización inicial del evento.', 1),
('REVISIÓN',     'Validación de la información y viabilidad del evento.', 2),
('PROGRAMACIÓN', 'Organización de actividades, horarios, responsables y recursos.', 3),
('DIFUSIÓN',     'Promoción y comunicación del evento.', 4),
('PREPARACIÓN',  'Preparación de espacios, recursos y personal.', 5),
('EN CURSO',     'Desarrollo del evento.', 6),
('CIERRE',       'Evaluación y cierre del evento.', 7);
select * from TipoEtapa;
select * from etapas;
select * from CupoEvento;