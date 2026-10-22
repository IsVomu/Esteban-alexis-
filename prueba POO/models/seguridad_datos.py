import hashlib

from models.conexion import ConexionDB


class seguridad_datos:

    def __init__(self, id_seguridad=None, id_empleado=None, datos_personales=None):
        self.id_seguridad = id_seguridad
        self.id_empleado = id_empleado
        self.datos_personales = datos_personales 
        self.datos_personales_cifrados = None  

    def __str__(self):
        return (f"ID seguridad: {self.id_seguridad} | ID empleado: {self.id_empleado} | "
                f"datos cifrados: {self.datos_personales_cifrados}")

    @staticmethod
    def cifrarDatos(texto):

        return hashlib.sha256(texto.encode("utf-8")).hexdigest().upper()

    # ---------- CONSULTA ----------
    def obtenerTodos_seguridad_datos(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                """SELECT ID_SEGURIDAD, ID_EMPLEADO,
                          SUBSTR(DATOS_PERSONALES_CIFRADOS, 1, 16) || '...'
                     FROM SEGURIDAD_DATOS
                    ORDER BY ID_SEGURIDAD"""
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de seguridad de datos : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_seguridad_datos(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO SEGURIDAD_DATOS
                        (id_seguridad, id_empleado, datos_personales_cifrados)
                     VALUES
                        (:id, :emp, :cifrado)"""
            c.cursor.execute(sql, {
                "id": self.id_seguridad,
                "emp": self.id_empleado,
                "cifrado": self.cifrarDatos(self.datos_personales),
            })
            c.conexion.commit()
            print("¡Datos de seguridad insertados correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla seguridad_datos : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_seguridad_datos(self):
        c = None
        try:
            c = ConexionDB()
            if self.datos_personales:
                self.datos_personales_cifrados = self.cifrarDatos(self.datos_personales)

            sql = """UPDATE SEGURIDAD_DATOS
                        SET id_empleado = :emp,
                            datos_personales_cifrados = :cifrado
                      WHERE id_seguridad = :id"""
            c.cursor.execute(sql, {
                "emp": self.id_empleado,
                "cifrado": self.datos_personales_cifrados,
                "id": self.id_seguridad,
            })
            c.conexion.commit()
            print("¡Datos de seguridad actualizados correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_seguridad_datos(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            sql = """SELECT id_seguridad, id_empleado, datos_personales_cifrados
                       FROM SEGURIDAD_DATOS
                      WHERE id_seguridad = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_seguridad = fila[0]
                self.id_empleado = fila[1]
                self.datos_personales_cifrados = fila[2]
                self.datos_personales = None
                return True
            else:
                print("No se encontró un registro de seguridad con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar seguridad de datos por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_seguridad_datos(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM SEGURIDAD_DATOS WHERE id_seguridad = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe un registro de seguridad con ese ID.")
            else:
                print("¡Datos de seguridad eliminados correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
