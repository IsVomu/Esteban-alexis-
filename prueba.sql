CREATE TABLE usuario (
    id_usuario      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR2(100) NOT NULL,
    email           VARCHAR2(150) NOT NULL UNIQUE,
    telefono        VARCHAR2(20),
    contrasena_hash VARCHAR2(255) NOT NULL,
    rol             VARCHAR2(30)  NOT NULL
);

CREATE TABLE departamento (
    id_depto    NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre      VARCHAR2(100) NOT NULL,
    id_gerente  NUMBER  -- FK a empleado, se agrega después
);

CREATE TABLE empleado (
    id_usuario   NUMBER PRIMARY KEY,
    fecha_inicio DATE NOT NULL,
    salario      NUMBER(12,2) CHECK (salario >= 0),
    id_depto     NUMBER,
    CONSTRAINT fk_emp_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario),
    CONSTRAINT fk_emp_depto FOREIGN KEY (id_depto)
        REFERENCES departamento (id_depto)
);

-- Se agrega después para evitar la dependencia circular
ALTER TABLE departamento
    ADD CONSTRAINT fk_depto_gerente FOREIGN KEY (id_gerente)
        REFERENCES empleado (id_usuario);

CREATE TABLE proyecto (
    id_proyecto  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre       VARCHAR2(100) NOT NULL,
    descripcion  VARCHAR2(500),
    fecha_inicio DATE
);

CREATE TABLE empleado_proyecto (
    id_empleado NUMBER NOT NULL,
    id_proyecto NUMBER NOT NULL,
    CONSTRAINT pk_emp_proy PRIMARY KEY (id_empleado, id_proyecto),
    CONSTRAINT fk_ep_emp FOREIGN KEY (id_empleado)
        REFERENCES empleado (id_usuario),
    CONSTRAINT fk_ep_proy FOREIGN KEY (id_proyecto)
        REFERENCES proyecto (id_proyecto)
);

CREATE TABLE registro_tiempo (
    id_registro       NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha             DATE NOT NULL,
    horas_trabajadas  NUMBER(4,2) NOT NULL CHECK (horas_trabajadas > 0 AND horas_trabajadas <= 24),
    descripcion_tarea VARCHAR2(500),
    estado            VARCHAR2(20) DEFAULT 'PENDIENTE' NOT NULL
                      CHECK (estado IN ('PENDIENTE','APROBADO','RECHAZADO')),
    fecha_aprobacion  DATE,
    id_empleado       NUMBER NOT NULL,
    id_proyecto       NUMBER NOT NULL,
    id_aprobador      NUMBER,
    CONSTRAINT fk_rt_emp FOREIGN KEY (id_empleado)
        REFERENCES empleado (id_usuario),
    CONSTRAINT fk_rt_proy FOREIGN KEY (id_proyecto)
        REFERENCES proyecto (id_proyecto),
    CONSTRAINT fk_rt_aprob FOREIGN KEY (id_aprobador)
        REFERENCES empleado (id_usuario)
);

--------------------------------------------------------------------------------
--Tabla             | Filas
--usuario           | 12
--departamento      | 10
--empleado          | 12
--proyecto          | 10
--empleado_proyecto | 21
--registro_tiempo   | 25

-- 1) USUARIO (12)
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Camila Rojas',      'camila.rojas@empresa.cl',      '+56911111111', 'hash_cam001', 'GERENTE');
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Matías Fuentes',    'matias.fuentes@empresa.cl',    '+56922222222', 'hash_mat002', 'GERENTE');
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Valentina Soto',    'valentina.soto@empresa.cl',    '+56933333333', 'hash_val003', 'GERENTE');
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Felipe Araya',      'felipe.araya@empresa.cl',      '+56944444444', 'hash_fel004', 'GERENTE');
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Javiera Muñoz',     'javiera.munoz@empresa.cl',     '+56955555555', 'hash_jav005', 'GERENTE');
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Sebastián Díaz',    'sebastian.diaz@empresa.cl',    '+56966666666', 'hash_seb006', 'EMPLEADO');
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Francisca Herrera', 'francisca.herrera@empresa.cl', '+56977777777', 'hash_fra007', 'EMPLEADO');
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Diego Castillo',    'diego.castillo@empresa.cl',    '+56988888888', 'hash_die008', 'EMPLEADO');
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Constanza Vega',    'constanza.vega@empresa.cl',    '+56999999999', 'hash_con009', 'EMPLEADO');
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Nicolás Pizarro',   'nicolas.pizarro@empresa.cl',   '+56910101010', 'hash_nic010', 'EMPLEADO');
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Catalina Reyes',    'catalina.reyes@empresa.cl',    '+56912121212', 'hash_cat011', 'EMPLEADO');
INSERT INTO usuario (nombre, email, telefono, contrasena_hash, rol) VALUES ('Tomás Contreras',   'tomas.contreras@empresa.cl',   NULL,           'hash_tom012', 'EMPLEADO');

-- 2) DEPARTAMENTO (10) - el gerente se asigna después
INSERT INTO departamento (nombre) VALUES ('Tecnología');
INSERT INTO departamento (nombre) VALUES ('Recursos Humanos');
INSERT INTO departamento (nombre) VALUES ('Finanzas');
INSERT INTO departamento (nombre) VALUES ('Marketing');
INSERT INTO departamento (nombre) VALUES ('Operaciones');
INSERT INTO departamento (nombre) VALUES ('Ventas');
INSERT INTO departamento (nombre) VALUES ('Soporte');
INSERT INTO departamento (nombre) VALUES ('Calidad');
INSERT INTO departamento (nombre) VALUES ('Legal');
INSERT INTO departamento (nombre) VALUES ('Logística');

-- 3) EMPLEADO (12) - id_usuario coincide con USUARIO
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (1,  DATE '2019-03-01', 2500000, 1);
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (2,  DATE '2018-07-15', 2400000, 2);
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (3,  DATE '2020-01-10', 2300000, 3);
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (4,  DATE '2019-09-02', 2200000, 4);
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (5,  DATE '2021-04-19', 2100000, 5);
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (6,  DATE '2021-08-23', 1400000, 1);
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (7,  DATE '2022-02-14', 1350000, 1);
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (8,  DATE '2022-05-30', 1200000, 2);
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (9,  DATE '2023-01-09', 1250000, 3);
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (10, DATE '2023-06-12', 1100000, 6);
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (11, DATE '2024-03-04', 1150000, 7);
INSERT INTO empleado (id_usuario, fecha_inicio, salario, id_depto) VALUES (12, DATE '2024-10-21', 1000000, NULL);

-- Asignar gerentes (departamentos 6 al 10 quedan sin gerente)
UPDATE departamento SET id_gerente = 1 WHERE id_depto = 1;
UPDATE departamento SET id_gerente = 2 WHERE id_depto = 2;
UPDATE departamento SET id_gerente = 3 WHERE id_depto = 3;
UPDATE departamento SET id_gerente = 4 WHERE id_depto = 4;
UPDATE departamento SET id_gerente = 5 WHERE id_depto = 5;

-- 4) PROYECTO (10)
INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES ('Sistema de Cabañas',     'Plataforma web de arriendo de cabañas',       DATE '2026-01-12');
INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES ('Portal de Clientes',     'Portal de autoatención para clientes',        DATE '2026-02-02');
INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES ('Migración a la Nube',    'Traslado de servidores a infraestructura cloud', DATE '2026-02-16');
INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES ('App Móvil Corporativa',  'Aplicación móvil para uso interno',           DATE '2026-03-01');
INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES ('Rediseño de Intranet',   'Nueva intranet con gestión documental',       DATE '2026-03-23');
INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES ('Campaña Verano',         'Campaña de marketing digital de temporada',   DATE '2026-04-06');
INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES ('Sistema de Inventario',  'Control de stock en bodegas',                 DATE '2026-04-20');
INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES ('Auditoría Interna 2026', 'Revisión de procesos y cumplimiento',         DATE '2026-05-04');
INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES ('Tablero de Indicadores', 'Dashboard de KPIs para gerencia',            DATE '2026-05-18');
INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES ('Soporte Nivel 2',        'Mejora del servicio de soporte técnico',      DATE '2026-06-01');

-- 5) EMPLEADO_PROYECTO (21)
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (1, 1);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (2, 2);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (3, 3);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (4, 1);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (4, 2);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (5, 1);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (5, 3);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (6, 1);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (6, 4);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (7, 2);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (7, 5);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (8, 3);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (8, 6);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (9, 4);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (9, 7);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (10, 5);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (10, 8);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (11, 6);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (11, 9);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (12, 7);
INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (12, 10);

-- 6) REGISTRO_TIEMPO (25)
-- columnas: fecha, horas, descripcion, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-01', 8,   'Diseño de base de datos',      'APROBADO',  DATE '2026-09-02', 4,  1, 1);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-01', 6.5, 'Revisión de requerimientos',   'APROBADO',  DATE '2026-09-02', 5,  1, 1);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-02', 7,   'Desarrollo módulo login',    'APROBADO',  DATE '2026-09-03', 6,  1, 1);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-02', 4,   'Reunión de planificación',   'APROBADO',  DATE '2026-09-03', 4,  2, 2);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-03', 8,   'Pruebas de integración',    'APROBADO',  DATE '2026-09-04', 7,  2, 2);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-03', 5.5, 'Configuración de servidor',  'APROBADO',  DATE '2026-09-04', 5,  3, 3);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-04', 7.5, 'Desarrollo API REST',        'APROBADO',  DATE '2026-09-05', 6,  4, 1);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-04', 6,   'Análisis de datos de ventas','APROBADO', DATE '2026-09-05', 8,  3, 3);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-07', 8,   'Campaña en redes sociales', 'APROBADO',  DATE '2026-09-08', 8,  6, 1);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-07', 3.5, 'Capacitación de usuarios',   'APROBADO',  DATE '2026-09-08', 9,  4, 1);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-08', 7,   'Documentación técnica',     'PENDIENTE', NULL,              9,  7, NULL);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-08', 8,   'Soporte a clientes',         'PENDIENTE', NULL,              10, 5, NULL);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-09', 6,   'Auditoría de procesos',     'APROBADO',  DATE '2026-09-10', 10, 8, 2);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-09', 9,   'Optimización de consultas', 'RECHAZADO', DATE '2026-09-10', 11, 6, 1);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-10', 5,   'Elaboración de informe',    'PENDIENTE', NULL,              11, 9, NULL);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-10', 7.5, 'Control de calidad',        'APROBADO',  DATE '2026-09-11', 12, 7, 2);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-11', 4.5, 'Mantención de equipos',     'PENDIENTE', NULL,              12, 10, NULL);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-11', 8,   'Supervisión de avance',     'APROBADO',  DATE '2026-09-12', 1,  1, 2);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-14', 6,   'Revisión de presupuesto',   'APROBADO',  DATE '2026-09-15', 2,  2, 1);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-14', 7,   'Coordinación de equipo',    'APROBADO',  DATE '2026-09-15', 3,  3, 1);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-15', 8,   'Desarrollo módulo reportes','PENDIENTE', NULL,              6,  4, NULL);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-15', 5,   'Pruebas de aceptación',    'RECHAZADO', DATE '2026-09-16', 7,  5, 2);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-16', 6.5, 'Migración de datos',        'APROBADO',  DATE '2026-09-17', 5,  1, 1);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-16', 7,   'Diseño de interfaz',        'PENDIENTE', NULL,              4,  1, NULL);
INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, estado, fecha_aprobacion, id_empleado, id_proyecto, id_aprobador) VALUES (DATE '2026-09-17', 4,   'Reunión con cliente',       'APROBADO',  DATE '2026-09-18', 9,  7, 3);

COMMIT;

--------------------------------------------------------------------------------

