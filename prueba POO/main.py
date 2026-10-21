from datetime import datetime

from models.administrador import administrador
from models.asignacion_departamento import asignacion_departamento
from models.asignacion_proyecto import asignacion_proyecto
from models.autenticacion import autenticacion
from models.departamento import departamento
from models.empleado import empleado
from models.informe import informe
from models.proyecto import proyecto
from models.registro_tiempo import registro_tiempo
from models.trabajador import trabajador


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
}

PISTAS = {"fecha": " (DD-MM-YYYY)", "decimal": " (ej: 7.5)"}
ESPERADO = {
    "int": "un número entero",
    "decimal": "un número (ej: 7.5)",
    "fecha": "una fecha con formato DD-MM-YYYY",
}


#------MENUS----
def imprimirMenu():
    print("Elige una de las siguientes opciones:")
    print("1. Ver todos los datos")
    print("2. Agregar datos")
    print("3. Actualizar datos")
    print("4. Eliminar Dato")
    print("0. Salir")


def menuTablas():
    print("De que tabla quieres hacer esta operacion:")
    for numero, tabla in TABLAS.items():
        print(f"{numero}- {tabla['titulo']}")
    print("0- Volver")



# ---------- FUNCIONES DE APOYO --------------
def leer_entero(mensaje):
    try:
        return int(input(mensaje).strip())
    except ValueError:
        print("ERROR: debes ingresar un número entero.\n")
        return None


def elegir_tabla():
    menuTablas()
    numero = leer_entero("Ingrese el numero de la tabla: ")
    if numero is None or numero == 0:
        print()
        return None
    if numero not in TABLAS:
        print("ERROR: esa tabla no existe en el menú.\n")
        return None
    print()
    return TABLAS[numero]


def metodo(objeto, prefijo, tabla):
    return getattr(objeto, f"{prefijo}_{tabla['sufijo']}")


def convertir(texto, tipo):
    if tipo == "int":
        return int(texto)
    if tipo == "decimal":
        return float(texto.replace(",", "."))
    if tipo == "fecha":
        datetime.strptime(texto, "%d-%m-%Y")
        return texto
    return texto


def pedir_campo(campo, actual=None, actualizando=False):
    atributo, etiqueta, tipo = campo
    pista = PISTAS.get(tipo, "")

    if actualizando:
        if tipo == "clave":
            texto = input(f"{etiqueta} [ENTER para no cambiarla]: ").strip()
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



#---------- OPERACIONES ---------------
def listar(tabla):
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



#------------------ PROGRAMA PRINCIPAL ---------------- 
ACCIONES = {1: listar, 2: agregar, 3: actualizar, 4: eliminar}

while True:
    imprimirMenu()
    opcion = leer_entero("Ingresa una opción: ")
    print()

    if opcion is None:
        continue

    if opcion == 0:
        print("saliendo del programa...")
        break

    if opcion not in ACCIONES:
        print("ERROR: opción no válida.\n")
        continue

    tabla = elegir_tabla()
    if tabla is None:
        continue

    try:
        ACCIONES[opcion](tabla)
    except Exception as e:
        print(f"Hubo un error inesperado: {e}\n")
