
DROP TABLE inicio_sesion           CASCADE CONSTRAINTS PURGE;
DROP TABLE autenticacion           CASCADE CONSTRAINTS PURGE;
DROP TABLE seguridad_datos         CASCADE CONSTRAINTS PURGE;
DROP TABLE informe                 CASCADE CONSTRAINTS PURGE;
DROP TABLE registro_tiempo         CASCADE CONSTRAINTS PURGE;
DROP TABLE asignacion_departamento CASCADE CONSTRAINTS PURGE;
DROP TABLE asignacion_proyecto     CASCADE CONSTRAINTS PURGE;
DROP TABLE proyecto                CASCADE CONSTRAINTS PURGE;
DROP TABLE administrador           CASCADE CONSTRAINTS PURGE;
DROP TABLE empleado                CASCADE CONSTRAINTS PURGE;
DROP TABLE trabajador              CASCADE CONSTRAINTS PURGE;
DROP TABLE departamento            CASCADE CONSTRAINTS PURGE;


-- Clase: Departamento
CREATE TABLE departamento (
    id_departamento  NUMBER(4)      NOT NULL,
    nombre           VARCHAR2(60)   NOT NULL,
    gerente_asociado VARCHAR2(80)   NOT NULL,
    CONSTRAINT pk_departamento PRIMARY KEY (id_departamento),
    CONSTRAINT uq_departamento_nombre UNIQUE (nombre)
);

-- Clase: trabajadores (superclase de Empleado y Administrador)
CREATE TABLE trabajador (
    id_empleado       NUMBER(6)      NOT NULL,
    nombre            VARCHAR2(80)   NOT NULL,
    direccion         VARCHAR2(120)  NOT NULL,
    numero_telefono   VARCHAR2(15)   NOT NULL,
    correo_electronico VARCHAR2(100) NOT NULL,
    inicio_contrato   DATE           NOT NULL,
    salario           NUMBER(10)     NOT NULL,
    id_departamento   NUMBER(4)      NOT NULL,
    CONSTRAINT pk_trabajador PRIMARY KEY (id_empleado),
    CONSTRAINT uq_trabajador_correo UNIQUE (correo_electronico),
    CONSTRAINT ck_trabajador_salario CHECK (salario > 0),
    CONSTRAINT fk_trabajador_depto FOREIGN KEY (id_departamento)
        REFERENCES departamento (id_departamento)
);

-- Clase: Empleado (hereda de trabajadores)
CREATE TABLE empleado (
    id_empleado NUMBER(6)     NOT NULL,
    cargo       VARCHAR2(60)  NOT NULL,
    CONSTRAINT pk_empleado PRIMARY KEY (id_empleado),
    CONSTRAINT fk_empleado_trabajador FOREIGN KEY (id_empleado)
        REFERENCES trabajador (id_empleado)
);

-- Clase: Administrador (hereda de trabajadores)
CREATE TABLE administrador (
    id_empleado      NUMBER(6) NOT NULL,
    nivel_privilegio NUMBER(2) NOT NULL,
    CONSTRAINT pk_administrador PRIMARY KEY (id_empleado),
    CONSTRAINT fk_administrador_trabajador FOREIGN KEY (id_empleado)
        REFERENCES trabajador (id_empleado),
    CONSTRAINT ck_admin_nivel CHECK (nivel_privilegio BETWEEN 1 AND 5)
);

-- Clase: Proyecto
CREATE TABLE proyecto (
    id_proyecto  NUMBER(4)      NOT NULL,
    nombre       VARCHAR2(80)   NOT NULL,
    descripcion  VARCHAR2(200)  NOT NULL,
    fecha_inicio DATE           NOT NULL,
    CONSTRAINT pk_proyecto PRIMARY KEY (id_proyecto)
);

-- Clase: Asignacion Proyectos a Empleados (Proyecto 0..* <-> 0..* trabajadores)
CREATE TABLE asignacion_proyecto (
    id_asignacion    NUMBER(6) NOT NULL,
    id_proyecto      NUMBER(4) NOT NULL,
    id_empleado      NUMBER(6) NOT NULL,
    fecha_asignacion DATE      NOT NULL,
    CONSTRAINT pk_asignacion_proyecto PRIMARY KEY (id_asignacion),
    CONSTRAINT uq_asig_proy_emp UNIQUE (id_proyecto, id_empleado),
    CONSTRAINT fk_asigproy_proyecto FOREIGN KEY (id_proyecto)
        REFERENCES proyecto (id_proyecto),
    CONSTRAINT fk_asigproy_trabajador FOREIGN KEY (id_empleado)
        REFERENCES trabajador (id_empleado)
);

-- Clase: Asignacion Dept Empleados (trabajadores -> Departamento)
CREATE TABLE asignacion_departamento (
    id_asignacion    NUMBER(6) NOT NULL,
    id_empleado      NUMBER(6) NOT NULL,
    id_departamento  NUMBER(4) NOT NULL,
    fecha_asignacion DATE      NOT NULL,
    CONSTRAINT pk_asignacion_depto PRIMARY KEY (id_asignacion),
    CONSTRAINT fk_asigdep_trabajador FOREIGN KEY (id_empleado)
        REFERENCES trabajador (id_empleado),
    CONSTRAINT fk_asigdep_depto FOREIGN KEY (id_departamento)
        REFERENCES departamento (id_departamento)
);

-- Clase: Registro Tiempo (trabajador 1..0..* y Proyecto 1..0..*)
CREATE TABLE registro_tiempo (
    id_registro             NUMBER(6)     NOT NULL,
    fecha                   DATE          NOT NULL,
    cantidad_horas_trabajadas NUMBER(4,1) NOT NULL,
    descripcion             VARCHAR2(150) NOT NULL,
    id_empleado             NUMBER(6)     NOT NULL,
    id_proyecto             NUMBER(4)     NOT NULL,
    CONSTRAINT pk_registro_tiempo PRIMARY KEY (id_registro),
    CONSTRAINT ck_registro_horas CHECK (cantidad_horas_trabajadas > 0 AND cantidad_horas_trabajadas <= 24),
    CONSTRAINT fk_registro_trabajador FOREIGN KEY (id_empleado)
        REFERENCES trabajador (id_empleado),
    CONSTRAINT fk_registro_proyecto FOREIGN KEY (id_proyecto)
        REFERENCES proyecto (id_proyecto)
);

-- Clase: informe (Administrador 1 genera 1..* informes)
CREATE TABLE informe (
    id_informe           NUMBER(6)     NOT NULL,
    informacion_empleado VARCHAR2(150) NOT NULL,
    proyectos            VARCHAR2(150) NOT NULL,
    departamento         VARCHAR2(80)  NOT NULL,
    registro_de_tiempo   VARCHAR2(150) NOT NULL,
    fecha_generacion     DATE          NOT NULL,
    id_administrador     NUMBER(6)     NOT NULL,
    CONSTRAINT pk_informe PRIMARY KEY (id_informe),
    CONSTRAINT fk_informe_admin FOREIGN KEY (id_administrador)
        REFERENCES administrador (id_empleado)
);

-- Clase: Seguridad de Datos Sensibles (agregación con trabajadores)
CREATE TABLE seguridad_datos (
    id_seguridad                NUMBER(6)     NOT NULL,
    id_empleado                 NUMBER(6)     NOT NULL,
    datos_personales_cifrados   VARCHAR2(100) NOT NULL,
    CONSTRAINT pk_seguridad_datos PRIMARY KEY (id_seguridad),
    CONSTRAINT uq_seguridad_empleado UNIQUE (id_empleado),
    CONSTRAINT fk_seguridad_trabajador FOREIGN KEY (id_empleado)
        REFERENCES trabajador (id_empleado)
);

-- Clase: Autenticación y autorizaciones (credenciales de cada trabajador)
CREATE TABLE autenticacion (
    id_autenticacion NUMBER(6)     NOT NULL,
    id_empleado      NUMBER(6)     NOT NULL,
    solo_usuario     VARCHAR2(100) NOT NULL,
    contrasena_hash  VARCHAR2(64)  NOT NULL,
    CONSTRAINT pk_autenticacion PRIMARY KEY (id_autenticacion),
    CONSTRAINT uq_autenticacion_empleado UNIQUE (id_empleado),
    CONSTRAINT uq_autenticacion_usuario UNIQUE (solo_usuario),
    CONSTRAINT fk_autenticacion_trabajador FOREIGN KEY (id_empleado)
        REFERENCES trabajador (id_empleado)
);

-- Clase: Inicio de Sesión (registro de cada intento de login)
CREATE TABLE inicio_sesion (
    id_sesion        NUMBER(6)     NOT NULL,
    id_autenticacion NUMBER(6)     NOT NULL,
    correo           VARCHAR2(100) NOT NULL,
    fecha_hora       TIMESTAMP     NOT NULL,
    exitoso          CHAR(1)       NOT NULL,
    CONSTRAINT pk_inicio_sesion PRIMARY KEY (id_sesion),
    CONSTRAINT ck_sesion_exitoso CHECK (exitoso IN ('S','N')),
    CONSTRAINT fk_sesion_autenticacion FOREIGN KEY (id_autenticacion)
        REFERENCES autenticacion (id_autenticacion)
);

-- ---------------------------------------------------------------------
-- 2. INSERCIÓN DE DATOS (respetando el orden de las FK)
-- ---------------------------------------------------------------------

-- DEPARTAMENTO (10 filas)
INSERT ALL
  INTO departamento VALUES (1,  'Recursos Humanos',      'Carolina Fuentes')
  INTO departamento VALUES (2,  'Tecnología',            'Rodrigo Miranda')
  INTO departamento VALUES (3,  'Finanzas',              'Patricia Soto')
  INTO departamento VALUES (4,  'Marketing',             'Camila Herrera')
  INTO departamento VALUES (5,  'Operaciones',           'Marcela Rojas')
  INTO departamento VALUES (6,  'Ventas',                'Sebastián Muñoz')
  INTO departamento VALUES (7,  'Soporte Técnico',       'Daniela Vargas')
  INTO departamento VALUES (8,  'Desarrollo de Software','Andrés Valdés')
  INTO departamento VALUES (9,  'Calidad',               'Francisca Lagos')
  INTO departamento VALUES (10, 'Sostenibilidad',        'Tomás Espinoza')
SELECT 1 FROM dual;

-- TRABAJADOR (20 filas: 1-10 administradores, 11-20 empleados)
INSERT ALL
  INTO trabajador VALUES (1,  'Carolina Fuentes',  'Av. Providencia 1234, Providencia',  '+56987650001', 'carolina.fuentes@ecotech.cl',  DATE '2018-03-01', 3200000, 1)
  INTO trabajador VALUES (2,  'Rodrigo Miranda',   'Los Leones 456, Providencia',        '+56987650002', 'rodrigo.miranda@ecotech.cl',   DATE '2018-06-15', 3000000, 2)
  INTO trabajador VALUES (3,  'Patricia Soto',     'Av. Apoquindo 3000, Las Condes',     '+56987650003', 'patricia.soto@ecotech.cl',     DATE '2018-11-05', 2900000, 3)
  INTO trabajador VALUES (4,  'Andrés Valdés',     'Av. Vitacura 2670, Vitacura',        '+56987650004', 'andres.valdes@ecotech.cl',     DATE '2019-02-10', 2800000, 8)
  INTO trabajador VALUES (5,  'Marcela Rojas',     'Irarrázaval 2100, Ñuñoa',            '+56987650005', 'marcela.rojas@ecotech.cl',     DATE '2019-09-01', 2600000, 5)
  INTO trabajador VALUES (6,  'Sebastián Muñoz',   'Av. Grecia 890, Ñuñoa',              '+56987650006', 'sebastian.munoz@ecotech.cl',   DATE '2020-01-13', 2500000, 6)
  INTO trabajador VALUES (7,  'Daniela Vargas',    'San Pablo 1560, Santiago',           '+56987650007', 'daniela.vargas@ecotech.cl',    DATE '2020-05-04', 2400000, 7)
  INTO trabajador VALUES (8,  'Camila Herrera',    'Av. La Florida 9500, La Florida',    '+56987650008', 'camila.herrera@ecotech.cl',    DATE '2020-10-05', 2450000, 4)
  INTO trabajador VALUES (9,  'Francisca Lagos',   'Av. Maipú 1200, Maipú',              '+56987650009', 'francisca.lagos@ecotech.cl',   DATE '2021-03-15', 2300000, 9)
  INTO trabajador VALUES (10, 'Tomás Espinoza',    'Av. Pajaritos 3300, Maipú',          '+56987650010', 'tomas.espinoza@ecotech.cl',    DATE '2021-06-07', 2350000, 10)
  INTO trabajador VALUES (11, 'Felipe Contreras',  'Gran Avenida 5400, San Miguel',      '+56987650011', 'felipe.contreras@ecotech.cl',  DATE '2021-09-20', 1500000, 2)
  INTO trabajador VALUES (12, 'Valentina Araya',   'Av. Matta 750, Santiago',            '+56987650012', 'valentina.araya@ecotech.cl',   DATE '2022-01-17', 1700000, 8)
  INTO trabajador VALUES (13, 'Matías Pizarro',    'Av. Independencia 1800, Independencia','+56987650013','matias.pizarro@ecotech.cl',    DATE '2022-04-11', 1650000, 8)
  INTO trabajador VALUES (14, 'Javiera Bravo',     'Av. Recoleta 2500, Recoleta',        '+56987650014', 'javiera.bravo@ecotech.cl',     DATE '2022-08-22', 1400000, 3)
  INTO trabajador VALUES (15, 'Nicolás Castro',    'Av. Larraín 6000, La Reina',         '+56987650015', 'nicolas.castro@ecotech.cl',    DATE '2022-11-07', 1000000, 5)
  INTO trabajador VALUES (16, 'Constanza Reyes',   'Av. Departamental 1100, San Joaquín','+56987650016', 'constanza.reyes@ecotech.cl',   DATE '2023-02-13', 1200000, 4)
  INTO trabajador VALUES (17, 'Benjamín Ortiz',    'Av. Américo Vespucio 1500, Quilicura','+56987650017','benjamin.ortiz@ecotech.cl',     DATE '2023-05-15', 1300000, 9)
  INTO trabajador VALUES (18, 'Antonia Silva',     'Av. Colón 4500, Las Condes',         '+56987650018', 'antonia.silva@ecotech.cl',     DATE '2023-09-04', 1600000, 10)
  INTO trabajador VALUES (19, 'Diego Carrasco',    'Av. Tobalaba 2050, Providencia',     '+56987650019', 'diego.carrasco@ecotech.cl',    DATE '2024-01-15',  950000, 7)
  INTO trabajador VALUES (20, 'Ignacio Tapia',     'Av. Quilín 3800, Peñalolén',         '+56987650020', 'ignacio.tapia@ecotech.cl',     DATE '2024-03-04', 1100000, 6)
SELECT 1 FROM dual;

-- ADMINISTRADOR (10 filas)
INSERT ALL
  INTO administrador VALUES (1,  5)
  INTO administrador VALUES (2,  4)
  INTO administrador VALUES (3,  4)
  INTO administrador VALUES (4,  4)
  INTO administrador VALUES (5,  3)
  INTO administrador VALUES (6,  3)
  INTO administrador VALUES (7,  3)
  INTO administrador VALUES (8,  3)
  INTO administrador VALUES (9,  2)
  INTO administrador VALUES (10, 2)
SELECT 1 FROM dual;

-- EMPLEADO (10 filas)
INSERT ALL
  INTO empleado VALUES (11, 'Analista de Sistemas')
  INTO empleado VALUES (12, 'Desarrolladora Backend')
  INTO empleado VALUES (13, 'Desarrollador Frontend')
  INTO empleado VALUES (14, 'Analista Contable')
  INTO empleado VALUES (15, 'Encargado de Bodega')
  INTO empleado VALUES (16, 'Diseñadora Gráfica')
  INTO empleado VALUES (17, 'Analista de Calidad')
  INTO empleado VALUES (18, 'Ingeniera Ambiental')
  INTO empleado VALUES (19, 'Técnico de Soporte')
  INTO empleado VALUES (20, 'Ejecutivo de Ventas')
SELECT 1 FROM dual;

-- PROYECTO (10 filas)
INSERT ALL
  INTO proyecto VALUES (1,  'Portal de Clientes EcoTech',      'Portal web para que los clientes gestionen sus servicios',      DATE '2024-01-10')
  INTO proyecto VALUES (2,  'Migración a la Nube',             'Traslado de servidores internos a infraestructura cloud',       DATE '2024-02-05')
  INTO proyecto VALUES (3,  'App Móvil de Reciclaje',          'Aplicación móvil para coordinar retiros de reciclaje',          DATE '2024-03-18')
  INTO proyecto VALUES (4,  'Sistema de Inventario Verde',     'Control de inventario de insumos ecológicos',                   DATE '2024-04-22')
  INTO proyecto VALUES (5,  'Panel de Huella de Carbono',      'Dashboard de medición de emisiones por área',                   DATE '2024-05-13')
  INTO proyecto VALUES (6,  'Automatización de Facturación',   'Emisión automática de facturas y notas de crédito',             DATE '2024-06-03')
  INTO proyecto VALUES (7,  'Campaña Marketing Sostenible',    'Campaña digital sobre prácticas sustentables',                  DATE '2024-07-08')
  INTO proyecto VALUES (8,  'Portal de Proveedores',           'Plataforma de gestión y evaluación de proveedores',             DATE '2024-08-19')
  INTO proyecto VALUES (9,  'Plataforma de Capacitación',      'Cursos en línea para el personal de la empresa',                DATE '2024-09-09')
  INTO proyecto VALUES (10, 'Monitoreo de Energía Solar',      'Sensores y reportes de producción de paneles solares',          DATE '2024-10-01')
SELECT 1 FROM dual;

-- ASIGNACION_PROYECTO (20 filas)
INSERT ALL
  INTO asignacion_proyecto VALUES (1,  1,  12, DATE '2024-01-15')
  INTO asignacion_proyecto VALUES (2,  1,  13, DATE '2024-01-15')
  INTO asignacion_proyecto VALUES (3,  2,  11, DATE '2024-02-10')
  INTO asignacion_proyecto VALUES (4,  2,  17, DATE '2024-02-10')
  INTO asignacion_proyecto VALUES (5,  3,  20, DATE '2024-03-25')
  INTO asignacion_proyecto VALUES (6,  3,  12, DATE '2024-03-25')
  INTO asignacion_proyecto VALUES (7,  4,  15, DATE '2024-04-29')
  INTO asignacion_proyecto VALUES (8,  4,  19, DATE '2024-04-29')
  INTO asignacion_proyecto VALUES (9,  5,  18, DATE '2024-05-20')
  INTO asignacion_proyecto VALUES (10, 5,  13, DATE '2024-05-20')
  INTO asignacion_proyecto VALUES (11, 6,  14, DATE '2024-06-10')
  INTO asignacion_proyecto VALUES (12, 6,  11, DATE '2024-06-10')
  INTO asignacion_proyecto VALUES (13, 7,  16, DATE '2024-07-15')
  INTO asignacion_proyecto VALUES (14, 7,  20, DATE '2024-07-15')
  INTO asignacion_proyecto VALUES (15, 8,  15, DATE '2024-08-26')
  INTO asignacion_proyecto VALUES (16, 8,  14, DATE '2024-08-26')
  INTO asignacion_proyecto VALUES (17, 9,  17, DATE '2024-09-16')
  INTO asignacion_proyecto VALUES (18, 9,  16, DATE '2024-09-16')
  INTO asignacion_proyecto VALUES (19, 10, 18, DATE '2024-10-07')
  INTO asignacion_proyecto VALUES (20, 10, 19, DATE '2024-10-07')
SELECT 1 FROM dual;

-- ASIGNACION_DEPARTAMENTO (20 filas, una por trabajador, tomada de TRABAJADOR)
INSERT INTO asignacion_departamento (id_asignacion, id_empleado, id_departamento, fecha_asignacion)
SELECT id_empleado, id_empleado, id_departamento, inicio_contrato
FROM trabajador;

-- REGISTRO_TIEMPO (25 filas; cada trabajador registra horas en proyectos que tiene asignados)
INSERT ALL
  INTO registro_tiempo VALUES (1,  DATE '2024-10-01', 8,   'Diseño de interfaz del portal',            12, 1)
  INTO registro_tiempo VALUES (2,  DATE '2024-10-01', 7.5, 'Desarrollo de interfaz de login',           13, 1)
  INTO registro_tiempo VALUES (3,  DATE '2024-10-02', 6,   'Configuración de servidores cloud',         11, 2)
  INTO registro_tiempo VALUES (4,  DATE '2024-10-02', 8,   'Pruebas de migración de base de datos',     17, 2)
  INTO registro_tiempo VALUES (5,  DATE '2024-10-03', 7,   'Prototipo de pantallas de la app',          20, 3)
  INTO registro_tiempo VALUES (6,  DATE '2024-10-03', 5.5, 'Revisión de requerimientos de la app',      12, 3)
  INTO registro_tiempo VALUES (7,  DATE '2024-10-04', 8,   'Carga inicial de inventario',               15, 4)
  INTO registro_tiempo VALUES (8,  DATE '2024-10-04', 6.5, 'Soporte a usuarios del inventario',         19, 4)
  INTO registro_tiempo VALUES (9,  DATE '2024-10-07', 7,   'Modelado de datos de emisiones',            18, 5)
  INTO registro_tiempo VALUES (10, DATE '2024-10-07', 8,   'Desarrollo de dashboards',                  13, 5)
  INTO registro_tiempo VALUES (11, DATE '2024-10-08', 6,   'Análisis de facturas históricas',           14, 6)
  INTO registro_tiempo VALUES (12, DATE '2024-10-08', 7.5, 'Script de automatización de facturas',      11, 6)
  INTO registro_tiempo VALUES (13, DATE '2024-10-09', 5,   'Diseño de piezas gráficas',                 16, 7)
  INTO registro_tiempo VALUES (14, DATE '2024-10-09', 8,   'Gestión de redes sociales',                 20, 7)
  INTO registro_tiempo VALUES (15, DATE '2024-10-10', 7,   'Levantamiento de proveedores',              15, 8)
  INTO registro_tiempo VALUES (16, DATE '2024-10-10', 6,   'Integración del catálogo de proveedores',   14, 8)
  INTO registro_tiempo VALUES (17, DATE '2024-10-11', 8,   'Elaboración de cursos',                     17, 9)
  INTO registro_tiempo VALUES (18, DATE '2024-10-11', 4.5, 'Revisión de calidad de contenidos',         16, 9)
  INTO registro_tiempo VALUES (19, DATE '2024-10-14', 7,   'Instalación de sensores',                   18, 10)
  INTO registro_tiempo VALUES (20, DATE '2024-10-14', 6.5, 'Pruebas de conectividad de sensores',       19, 10)
  INTO registro_tiempo VALUES (21, DATE '2024-10-15', 8,   'Desarrollo de API de clientes',             12, 1)
  INTO registro_tiempo VALUES (22, DATE '2024-10-15', 7,   'Optimización de consultas del portal',      13, 1)
  INTO registro_tiempo VALUES (23, DATE '2024-10-16', 6,   'Documentación técnica de la app',           20, 3)
  INTO registro_tiempo VALUES (24, DATE '2024-10-16', 7.5, 'Capacitación al equipo sobre la nube',      17, 2)
  INTO registro_tiempo VALUES (25, DATE '2024-10-17', 8,   'Validación de reportes de emisiones',       18, 5)
SELECT 1 FROM dual;

-- INFORME (12 filas, generados por administradores)
INSERT ALL
  INTO informe VALUES (1,  'Resumen de trabajadores activos',      'Todos los proyectos en curso',    'Todos los departamentos', 'Horas registradas en octubre 2024', DATE '2024-10-18', 1)
  INTO informe VALUES (2,  'Equipo de Tecnología',                 'Migración a la Nube',             'Tecnología',              'Horas registradas por semana',      DATE '2024-10-18', 2)
  INTO informe VALUES (3,  'Equipo de Finanzas',                   'Automatización de Facturación',   'Finanzas',                'Horas registradas por semana',      DATE '2024-10-18', 3)
  INTO informe VALUES (4,  'Equipo de Desarrollo de Software',     'Portal de Clientes EcoTech',      'Desarrollo de Software',  'Horas registradas por semana',      DATE '2024-10-18', 4)
  INTO informe VALUES (5,  'Equipo de Operaciones',                'Sistema de Inventario Verde',     'Operaciones',             'Horas registradas por semana',      DATE '2024-10-18', 5)
  INTO informe VALUES (6,  'Equipo de Ventas',                     'Campaña Marketing Sostenible',    'Ventas',                  'Horas registradas por semana',      DATE '2024-10-19', 6)
  INTO informe VALUES (7,  'Equipo de Soporte Técnico',            'Monitoreo de Energía Solar',      'Soporte Técnico',         'Horas registradas por semana',      DATE '2024-10-19', 7)
  INTO informe VALUES (8,  'Equipo de Marketing',                  'Campaña Marketing Sostenible',    'Marketing',               'Horas registradas por semana',      DATE '2024-10-19', 8)
  INTO informe VALUES (9,  'Equipo de Calidad',                    'Plataforma de Capacitación',      'Calidad',                 'Horas registradas por semana',      DATE '2024-10-20', 9)
  INTO informe VALUES (10, 'Equipo de Sostenibilidad',             'Panel de Huella de Carbono',      'Sostenibilidad',          'Horas registradas por semana',      DATE '2024-10-20', 10)
  INTO informe VALUES (11, 'Informe de contrataciones 2024',       'No aplica',                       'Recursos Humanos',        'No aplica',                         DATE '2024-10-20', 1)
  INTO informe VALUES (12, 'Informe de carga horaria por proyecto','Todos los proyectos en curso',    'Tecnología',              'Horas totales por proyecto',        DATE '2024-10-20', 2)
SELECT 1 FROM dual;

-- SEGURIDAD_DATOS (20 filas): dirección y teléfono cifrados con SHA-256
INSERT INTO seguridad_datos (id_seguridad, id_empleado, datos_personales_cifrados)
SELECT id_empleado,
       id_empleado,
       RAWTOHEX(STANDARD_HASH(direccion || numero_telefono, 'SHA256'))
FROM trabajador;

-- AUTENTICACION (20 filas): usuario = correo, contraseña almacenada como hash SHA-256
INSERT INTO autenticacion (id_autenticacion, id_empleado, solo_usuario, contrasena_hash)
SELECT id_empleado,
       id_empleado,
       correo_electronico,
       RAWTOHEX(STANDARD_HASH('Clave' || id_empleado || '#2024', 'SHA256'))
FROM trabajador;

-- INICIO_SESION (20 filas): un intento por usuario; cada 7° intento falla
INSERT INTO inicio_sesion (id_sesion, id_autenticacion, correo, fecha_hora, exitoso)
SELECT a.id_autenticacion,
       a.id_autenticacion,
       a.solo_usuario,
       TIMESTAMP '2024-10-21 08:00:00' + NUMTODSINTERVAL(a.id_autenticacion * 7, 'MINUTE'),
       CASE WHEN MOD(a.id_autenticacion, 7) = 0 THEN 'N' ELSE 'S' END
FROM autenticacion a;

COMMIT;

-- ---------------------------------------------------------------------
-- 3. VERIFICACIÓN: cantidad de filas por tabla (debe ser 10 a 30)
-- ---------------------------------------------------------------------
SELECT 'DEPARTAMENTO' tabla, COUNT(*) filas FROM departamento UNION ALL
SELECT 'TRABAJADOR',              COUNT(*) FROM trabajador              UNION ALL
SELECT 'ADMINISTRADOR',           COUNT(*) FROM administrador           UNION ALL
SELECT 'EMPLEADO',                COUNT(*) FROM empleado                UNION ALL
SELECT 'PROYECTO',                COUNT(*) FROM proyecto                UNION ALL
SELECT 'ASIGNACION_PROYECTO',     COUNT(*) FROM asignacion_proyecto     UNION ALL
SELECT 'ASIGNACION_DEPARTAMENTO', COUNT(*) FROM asignacion_departamento UNION ALL
SELECT 'REGISTRO_TIEMPO',         COUNT(*) FROM registro_tiempo         UNION ALL
SELECT 'INFORME',                 COUNT(*) FROM informe                 UNION ALL
SELECT 'SEGURIDAD_DATOS',         COUNT(*) FROM seguridad_datos         UNION ALL
SELECT 'AUTENTICACION',           COUNT(*) FROM autenticacion           UNION ALL
SELECT 'INICIO_SESION',           COUNT(*) FROM inicio_sesion;

-- Ejemplo de consulta con JOIN: horas trabajadas por trabajador y proyecto
SELECT t.nombre, p.nombre AS proyecto, SUM(r.cantidad_horas_trabajadas) AS total_horas
FROM registro_tiempo r
JOIN trabajador t ON t.id_empleado = r.id_empleado
JOIN proyecto   p ON p.id_proyecto = r.id_proyecto
GROUP BY t.nombre, p.nombre
ORDER BY t.nombre, p.nombre;