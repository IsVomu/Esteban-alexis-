from models.conexion import ConexionDB


class administrador:
    def __init__(self, id_empleado=None, nivel_privilegio=None):
        self.id_empleado = id_empleado
        self.nivel_privilegio = nivel_privilegio

    def __str__(self):
        return f"ID empleado: {self.id_empleado} | nivel de privilegio: {self.nivel_privilegio}"

    # ---------- ¿ES ADMINISTRADOR? ----------
    def esAdministrador(self, idEmpleado):

        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "SELECT COUNT(*) FROM ADMINISTRADOR WHERE id_empleado = :id",
                {"id": idEmpleado}
            )
            return c.cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"ERROR al comprobar si es administrador : {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- CONSULTA ----------
    def obtenerTodos_administrador(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "SELECT ID_EMPLEADO, NIVEL_PRIVILEGIO FROM ADMINISTRADOR ORDER BY ID_EMPLEADO"
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de los administradores : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_administrador(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO ADMINISTRADOR
                        (id_empleado, nivel_privilegio)
                     VALUES
                        (:id, :niv)"""
            c.cursor.execute(sql, {
                "id": self.id_empleado,
                "niv": self.nivel_privilegio,
            })
            c.conexion.commit()
            print("¡Administrador insertado correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla administrador : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_administrador(self):
        c = None
        try:
            c = ConexionDB()
            sql = """UPDATE ADMINISTRADOR
                        SET nivel_privilegio = :niv
                      WHERE id_empleado = :id"""
            c.cursor.execute(sql, {
                "niv": self.nivel_privilegio,
                "id": self.id_empleado,
            })
            c.conexion.commit()
            print("¡Administrador actualizado correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_administrador(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            sql = """SELECT id_empleado, nivel_privilegio
                       FROM ADMINISTRADOR
                      WHERE id_empleado = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_empleado = fila[0]
                self.nivel_privilegio = fila[1]
                return True
            else:
                print("No se encontró un administrador con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar administrador por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_administrador(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM ADMINISTRADOR WHERE id_empleado = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe un administrador con ese ID.")
            else:
                print("¡Administrador eliminado correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
