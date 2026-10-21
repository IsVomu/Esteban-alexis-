from models.conexion import ConexionDB


class asignacion_proyecto:
    def __init__(self, id_asignacion=None, id_proyecto=None, id_empleado=None, fecha_asignacion=None):
        self.id_asignacion = id_asignacion
        self.id_proyecto = id_proyecto
        self.id_empleado = id_empleado
        self.fecha_asignacion = fecha_asignacion

    def __str__(self):
        return (f"ID asignación: {self.id_asignacion} | ID proyecto: {self.id_proyecto} | "
                f"ID empleado: {self.id_empleado} | fecha: {self.fecha_asignacion}")

    # ---------- CONSULTA ----------
    def obtenerTodos_asignacion_proyecto(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                """SELECT ID_ASIGNACION, ID_PROYECTO, ID_EMPLEADO,
                          TO_CHAR(FECHA_ASIGNACION, 'DD-MM-YYYY')
                     FROM ASIGNACION_PROYECTO
                    ORDER BY ID_ASIGNACION"""
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de las asignaciones de proyecto : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_asignacion_proyecto(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO ASIGNACION_PROYECTO
                        (id_asignacion, id_proyecto, id_empleado, fecha_asignacion)
                     VALUES
                        (:id, :proy, :emp, TO_DATE(:fec, 'DD-MM-YYYY'))"""
            c.cursor.execute(sql, {
                "id": self.id_asignacion,
                "proy": self.id_proyecto,
                "emp": self.id_empleado,
                "fec": self.fecha_asignacion,
            })
            c.conexion.commit()
            print("¡Asignación de proyecto insertada correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla asignacion_proyecto : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_asignacion_proyecto(self):
        c = None
        try:
            c = ConexionDB()
            sql = """UPDATE ASIGNACION_PROYECTO
                        SET id_proyecto = :proy,
                            id_empleado = :emp,
                            fecha_asignacion = TO_DATE(:fec, 'DD-MM-YYYY')
                      WHERE id_asignacion = :id"""
            c.cursor.execute(sql, {
                "proy": self.id_proyecto,
                "emp": self.id_empleado,
                "fec": self.fecha_asignacion,
                "id": self.id_asignacion,
            })
            c.conexion.commit()
            print("¡Asignación de proyecto actualizada correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_asignacion_proyecto(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            sql = """SELECT id_asignacion, id_proyecto, id_empleado, fecha_asignacion
                       FROM ASIGNACION_PROYECTO
                      WHERE id_asignacion = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_asignacion = fila[0]
                self.id_proyecto = fila[1]
                self.id_empleado = fila[2]
                self.fecha_asignacion = fila[3].strftime("%d-%m-%Y") if fila[3] else ""
                return True
            else:
                print("No se encontró una asignación de proyecto con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar asignación de proyecto por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_asignacion_proyecto(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM ASIGNACION_PROYECTO WHERE id_asignacion = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe una asignación de proyecto con ese ID.")
            else:
                print("¡Asignación de proyecto eliminada correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
