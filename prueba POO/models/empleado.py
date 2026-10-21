from models.conexion import ConexionDB


class empleado:
    def __init__(self, id_empleado=None, cargo=None):
        self.id_empleado = id_empleado
        self.cargo = cargo

    def __str__(self):
        return f"ID empleado: {self.id_empleado} | cargo: {self.cargo}"

    # ---------- CONSULTA ----------
    def obtenerTodos_empleado(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "SELECT ID_EMPLEADO, CARGO FROM EMPLEADO ORDER BY ID_EMPLEADO"
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de los empleados : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_empleado(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO EMPLEADO
                        (id_empleado, cargo)
                     VALUES
                        (:id, :cargo)"""
            c.cursor.execute(sql, {
                "id": self.id_empleado,
                "cargo": self.cargo,
            })
            c.conexion.commit()
            print("¡Empleado insertado correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla empleado : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_empleado(self):
        c = None
        try:
            c = ConexionDB()
            sql = """UPDATE EMPLEADO
                        SET cargo = :cargo
                      WHERE id_empleado = :id"""
            c.cursor.execute(sql, {
                "cargo": self.cargo,
                "id": self.id_empleado,
            })
            c.conexion.commit()
            print("¡Empleado actualizado correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_empleado(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            sql = """SELECT id_empleado, cargo
                       FROM EMPLEADO
                      WHERE id_empleado = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_empleado = fila[0]
                self.cargo = fila[1]
                return True
            else:
                print("No se encontró un empleado con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar empleado por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_empleado(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM EMPLEADO WHERE id_empleado = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe un empleado con ese ID.")
            else:
                print("¡Empleado eliminado correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
