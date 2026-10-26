import getpass
from datetime import datetime

from models.administrador import administrador
from models.asignacion_departamento import asignacion_departamento
from models.asignacion_proyecto import asignacion_proyecto
from models.autenticacion import autenticacion
from models.departamento import departamento
from models.empleado import empleado
from models.informe import informe
from models.inicio_sesion import inicio_sesion
from models.proyecto import proyecto
from models.registro_tiempo import registro_tiempo
from models.seguridad_datos import seguridad_datos
from models.trabajador import trabajador


# ----------------------------------------------------------------------
# DESCRIPCIÓN DE LAS TABLAS
# Cada tabla se describe una sola vez y el resto del programa (listar,
# agregar, actualizar y eliminar) funciona igual para todas.
#
#   titulo : nombre que se muestra en los menús
#   clase  : clase de la carpeta models
#   sufijo : final del nombre de los métodos (insertar_<sufijo>, etc.)
#   campos : lista de (atributo de la clase, texto que se le muestra al usuario, tipo)
#            - el PRIMER campo siempre es el ID de la tabla
#            - el orden debe ser el mismo del SELECT de obtenerTodos_<sufijo>
#
# Tipos: "int" (entero), "decimal", "fecha" (DD-MM-YYYY), "fechahora" (DD-MM-YYYY HH:MM),
#        "sn" (S o N), "texto" y "clave" (texto que se guarda como hash)
# ----------------------------------------------------------------------
TABLAS = {
    1: {
        "titulo": "Administrador",
        "clase": administrador,
        "sufijo": "administrador",
        "campos": [
            ("id_empleado", "ID del trabajador", "int"),
            ("nivel_privilegio", "Nivel de privilegio (1 a 5)", "int"),
        ],
    },
    2: {
        "titulo": "Asignacion Departamento",
        "clase": asignacion_departamento,
        "sufijo": "asignacion_departamento",
        "campos": [
            ("id_asignacion", "ID de la asignación", "int"),
            ("id_empleado", "ID del trabajador", "int"),
            ("id_departamento", "ID del departamento", "int"),
            ("fecha_asignacion", "Fecha de asignación", "fecha"),
        ],
    },
    3: {
        "titulo": "Asignacion proyecto",
        "clase": asignacion_proyecto,
        "sufijo": "asignacion_proyecto",
        "campos": [
            ("id_asignacion", "ID de la asignación", "int"),
            ("id_proyecto", "ID del proyecto", "int"),
            ("id_empleado", "ID del trabajador", "int"),
            ("fecha_asignacion", "Fecha de asignación", "fecha"),
        ],
    },
    4: {
        "titulo": "Autenticacion",
        "clase": autenticacion,
        "sufijo": "autenticacion",
        "campos": [
            ("id_autenticacion", "ID de autenticación", "int"),
            ("id_empleado", "ID del trabajador", "int"),
            ("solo_usuario", "Usuario", "texto"),
            ("contrasena", "Contraseña", "clave"),
        ],
    },
    5: {
        "titulo": "Departamento",
        "clase": departamento,
        "sufijo": "departamento",
        "campos": [
            ("id_departamento", "ID del departamento", "int"),
            ("nombre", "Nombre", "texto"),
            ("gerente_asociado", "Gerente asociado", "texto"),
        ],
    },
    6: {
        "titulo": "Empleado",
        "clase": empleado,
        "sufijo": "empleado",
        "campos": [
            ("id_empleado", "ID del trabajador", "int"),
            ("cargo", "Cargo", "texto"),
        ],
    },
    7: {
        "titulo": "Informe",
        "clase": informe,
        "sufijo": "informe",
        "campos": [
            ("id_informe", "ID del informe", "int"),
            ("informacion_empleado", "Información del empleado", "texto"),
            ("proyectos", "Proyectos", "texto"),
            ("departamento", "Departamento", "texto"),
            ("registro_de_tiempo", "Registro de tiempo", "texto"),
            ("fecha_generacion", "Fecha de generación", "fecha"),
            ("id_administrador", "ID del administrador", "int"),
        ],
    },
    8: {
        "titulo": "Proyecto",
        "clase": proyecto,
        "sufijo": "proyecto",
        "campos": [
            ("id_proyecto", "ID del proyecto", "int"),
            ("nombre", "Nombre", "texto"),
            ("descripcion", "Descripción", "texto"),
            ("fecha_inicio", "Fecha de inicio", "fecha"),
        ],
    },
    9: {
        "titulo": "Registro Tiempo",
        "clase": registro_tiempo,
        "sufijo": "registro_tiempo",
        "campos": [
            ("id_registro", "ID del registro", "int"),
            ("fecha", "Fecha", "fecha"),
            ("cantidad_horas_trabajadas", "Horas trabajadas", "decimal"),
            ("descripcion", "Descripción", "texto"),
            ("id_empleado", "ID del trabajador", "int"),
            ("id_proyecto", "ID del proyecto", "int"),
        ],
    },
    10: {
        "titulo": "Trabajador",
        "clase": trabajador,
        "sufijo": "trabajador",
        "campos": [
            ("id_empleado", "ID del trabajador", "int"),
            ("nombre", "Nombre", "texto"),
            ("direccion", "Dirección", "texto"),
            ("numero_telefono", "Teléfono", "texto"),
            ("correo_electronico", "Correo electrónico", "texto"),
            ("inicio_contrato", "Inicio de contrato", "fecha"),
            ("salario", "Salario", "int"),
            ("id_departamento", "ID del departamento", "int"),
        ],
    },
    11: {
        "titulo": "Inicio Sesion",
        "clase": inicio_sesion,
        "sufijo": "inicio_sesion",
        "campos": [
            ("id_sesion", "ID de la sesión", "int"),
            ("id_autenticacion", "ID de autenticación", "int"),
            ("correo", "Correo", "texto"),
            ("fecha_hora", "Fecha y hora", "fechahora"),
            ("exitoso", "Inicio exitoso", "sn"),
        ],
    },
    12: {
        "titulo": "Seguridad Datos",
        "clase": seguridad_datos,
        "sufijo": "seguridad_datos",
        "campos": [
            ("id_seguridad", "ID de seguridad", "int"),
            ("id_empleado", "ID del trabajador", "int"),
            ("datos_personales", "Datos personales a proteger", "clave"),
        ],
    },
}

PISTAS = {"fecha": " (DD-MM-YYYY)", "fechahora": " (DD-MM-YYYY HH:MM)",
          "decimal": " (ej: 7.5)", "sn": " (S/N)"}
ESPERADO = {
    "int": "un número entero",
    "decimal": "un número (ej: 7.5)",
    "fecha": "una fecha con formato DD-MM-YYYY",
    "fechahora": "una fecha y hora con formato DD-MM-YYYY HH:MM (ej: 21-10-2024 08:30)",
    "sn": "S (sí) o N (no)",
}


# ----------------------------------------------------------------------
# MENÚS
# ----------------------------------------------------------------------
def imprimirMenu(operaciones):
    # operaciones: {numero: (texto, funcion)} con lo que el usuario puede hacer
    print("Elige una de las siguientes opciones:")
    for numero, (texto, funcion) in operaciones.items():
        print(f"{numero}. {texto}")
    print("0. Cerrar sesión")


def menuTablas(tablas):
    # tablas: {numero: tabla} con las tablas que el usuario puede ver
    print("De que tabla quieres hacer esta operacion:")
    for numero, tabla in tablas.items():
        print(f"{numero}- {tabla['titulo']}")
    print("0- Volver")


# ----------------------------------------------------------------------
# FUNCIONES DE APOYO
# ----------------------------------------------------------------------
def leer_entero(mensaje):
    # Devuelve un entero, o None si lo ingresado no es un número entero
    try:
        return int(input(mensaje).strip())
    except ValueError:
        print("ERROR: debes ingresar un número entero.\n")
        return None


def elegir_tabla(tablas):
    # Muestra el menú de tablas permitidas y devuelve la tabla elegida (o None)
    menuTablas(tablas)
    numero = leer_entero("Ingrese el numero de la tabla: ")
    if numero is None or numero == 0:
        print()
        return None
    if numero not in tablas:
        print("ERROR: esa tabla no existe en el menú.\n")
        return None
    print()
    return tablas[numero]


def metodo(objeto, prefijo, tabla):
    # Busca el método según el nombre, por ejemplo insertar_departamento
    return getattr(objeto, f"{prefijo}_{tabla['sufijo']}")


def convertir(texto, tipo):
    # Convierte el texto ingresado al tipo del campo (lanza ValueError si no corresponde)
    if tipo == "int":
        return int(texto)
    if tipo == "decimal":
        return float(texto.replace(",", "."))
    if tipo == "fecha":
        datetime.strptime(texto, "%d-%m-%Y")   # solo valida el formato
        return texto
    if tipo == "fechahora":
        datetime.strptime(texto, "%d-%m-%Y %H:%M")   # solo valida el formato
        return texto
    if tipo == "sn":
        texto = texto.upper()
        if texto not in ("S", "N"):
            raise ValueError("solo se acepta S o N")
        return texto
    return texto                                # "texto" y "clave"


def pedir_campo(campo, actual=None, actualizando=False):
    # Pide un dato por teclado y lo devuelve ya convertido.
    # Al actualizar, ENTER conserva el valor actual.
    atributo, etiqueta, tipo = campo
    pista = PISTAS.get(tipo, "")

    if actualizando:
        if tipo == "clave":
            texto = input(f"{etiqueta} [ENTER para no cambiar]: ").strip()
        else:
            texto = input(f"{etiqueta}{pista} [{actual}]: ").strip()
        if texto == "":
            return actual
    else:
        texto = input(f"{etiqueta}{pista}: ").strip()
        if texto == "":
            raise ValueError(f"'{etiqueta}' es obligatorio.")

    try:
        return convertir(texto, tipo)
    except ValueError:
        raise ValueError(f"'{etiqueta}' no es válido, se esperaba {ESPERADO[tipo]}.")


# ----------------------------------------------------------------------
# OPERACIONES (valen para cualquier tabla)
# ----------------------------------------------------------------------
def listar(tabla):
    # Opción 1: muestra todos los registros. Devuelve la lista de filas.
    objeto = tabla["clase"]()
    filas = metodo(objeto, "obtenerTodos", tabla)()

    if not filas:
        print(f"No hay datos registrados en {tabla['titulo']}.\n")
        return []

    print(f"--- LISTA DE {tabla['titulo'].upper()} ---")
    for fila in filas:
        partes = [f"{campo[1]}: {valor}" for campo, valor in zip(tabla["campos"], fila)]
        print(" | ".join(partes))
    print()
    return filas


def agregar(tabla):
    # Opción 2: pide todos los datos y los inserta
    print(f"---AGREGAR {tabla['titulo'].upper()}---")
    print("*TODOS LOS DATOS SON OBLIGATORIOS*")

    objeto = tabla["clase"]()
    try:
        for campo in tabla["campos"]:
            setattr(objeto, campo[0], pedir_campo(campo))
    except ValueError as e:
        print(f"ERROR: {e}\n")
        return

    metodo(objeto, "insertar", tabla)()
    print()


def actualizar(tabla):
    # Opción 3: muestra los registros, carga el elegido y permite cambiar sus campos
    if not listar(tabla):
        return

    print(f"--- ACTUALIZAR {tabla['titulo'].upper()} ---")
    idSeleccionado = leer_entero("Ingresar el ID a actualizar: ")
    if idSeleccionado is None:
        return

    objeto = tabla["clase"]()
    if not metodo(objeto, "cargarPorID", tabla)(idSeleccionado):
        print()
        return

    print("\n(Presiona ENTER si no deseas modificar un campo)")
    try:
        # El primer campo es el ID y no se modifica
        for campo in tabla["campos"][1:]:
            atributo = campo[0]
            nuevo = pedir_campo(campo, getattr(objeto, atributo), actualizando=True)
            setattr(objeto, atributo, nuevo)
    except ValueError as e:
        print(f"ERROR: {e}\n")
        return

    metodo(objeto, "actualizar", tabla)()
    print()


def eliminar(tabla):
    # Opción 4: muestra los registros y elimina el elegido (con confirmación)
    if not listar(tabla):
        return

    print(f"--- ELIMINAR {tabla['titulo'].upper()} ---")
    idSeleccionado = leer_entero("Ingresa el ID a eliminar: ")
    if idSeleccionado is None:
        return

    confirmar = input(f"¿Seguro que quieres eliminar el ID {idSeleccionado}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Operación cancelada.\n")
        return

    objeto = tabla["clase"]()
    metodo(objeto, "eliminar", tabla)(idSeleccionado)
    print()


# ----------------------------------------------------------------------
# PERMISOS SEGÚN EL TIPO DE USUARIO
#
#   Administrador : todas las tablas y todas las operaciones.
#   Empleado      : solo las tablas de TABLAS_EMPLEADO y solo las operaciones
#                   de OPERACIONES_EMPLEADO (por ahora solo consultar).
#
# Los números de TABLAS_EMPLEADO son los del diccionario TABLAS:
#   2 Asignacion Departamento, 3 Asignacion proyecto, 5 Departamento,
#   7 Informe, 8 Proyecto, 10 Trabajador
# Si quieres que el empleado también pueda agregar, actualizar o eliminar,
# agrega 2, 3 o 4 a OPERACIONES_EMPLEADO.
# ----------------------------------------------------------------------
OPERACIONES = {
    1: ("Ver todos los datos", listar),
    2: ("Agregar datos", agregar),
    3: ("Actualizar datos", actualizar),
    4: ("Eliminar Dato", eliminar),
}

TABLAS_EMPLEADO = [5, 10, 8, 2, 3, 7]
OPERACIONES_EMPLEADO = [1]

MAX_INTENTOS = 3


# ----------------------------------------------------------------------
# INICIO DE SESIÓN
# ----------------------------------------------------------------------
def iniciar_sesion():
    # Pide usuario y contraseña (máximo MAX_INTENTOS intentos) y los valida contra
    # la tabla AUTENTICACION. Cada intento de un usuario que existe se guarda en
    # INICIO_SESION ("S" correcto, "N" contraseña incorrecta).
    # Devuelve un diccionario con los datos de la sesión, o None si no se pudo entrar.
    print("Ingresa tus credenciales (deja el usuario vacío y presiona ENTER para salir)")

    for intento in range(1, MAX_INTENTOS + 1):
        usuario = input("Usuario (correo): ").strip()
        if usuario == "":
            return None
        contrasena = getpass.getpass("Contraseña: ")

        aut = autenticacion()
        resultado = aut.validarUsuario(usuario, contrasena)

        if resultado == "ok":
            inicio_sesion().registrarInicio(aut.id_autenticacion, usuario, "S")

            esAdmin = administrador().esAdministrador(aut.id_empleado)

            persona = trabajador()
            nombre = persona.nombre if persona.cargarPorID_trabajador(aut.id_empleado) else usuario

            return {"id_empleado": aut.id_empleado, "nombre": nombre, "es_admin": esAdmin}

        if resultado == "clave_incorrecta":
            inicio_sesion().registrarInicio(aut.id_autenticacion, usuario, "N")

        # Mismo mensaje si el usuario no existe o la clave está mal (no se da pistas)
        print(f"ERROR: usuario o contraseña incorrectos. Intento {intento} de {MAX_INTENTOS}.\n")

    print("Demasiados intentos fallidos.")
    return None


# ----------------------------------------------------------------------
# MENÚ SEGÚN EL TIPO DE USUARIO
# ----------------------------------------------------------------------
def menu_sesion(sesion):
    if sesion["es_admin"]:
        rol = "Administrador"
        tablas = TABLAS
        operaciones = OPERACIONES
    else:
        rol = "Empleado"
        # Se renumeran de 1 en adelante para que el menú se vea ordenado
        tablas = {i: TABLAS[n] for i, n in enumerate(TABLAS_EMPLEADO, start=1)}
        operaciones = {n: OPERACIONES[n] for n in OPERACIONES_EMPLEADO}

    print(f"\n=== Bienvenido/a {sesion['nombre']} ({rol}) ===\n")

    while True:
        imprimirMenu(operaciones)
        opcion = leer_entero("Ingresa una opción: ")
        print()

        if opcion is None:
            continue

        if opcion == 0:
            print("Sesión cerrada.\n")
            return

        if opcion not in operaciones:
            print("ERROR: opción no válida.\n")
            continue

        tabla = elegir_tabla(tablas)
        if tabla is None:
            continue

        try:
            operaciones[opcion][1](tabla)
        except Exception as e:
            print(f"Hubo un error inesperado: {e}\n")


# ----------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ----------------------------------------------------------------------
while True:
    print("=== SISTEMA DE GESTIÓN INTERNA - ECOTECH SOLUTIONS ===")
    sesion = iniciar_sesion()
    if sesion is None:
        print("saliendo del programa...")
        break
    menu_sesion(sesion)
