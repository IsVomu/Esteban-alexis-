from models.conexion import ConexionDB


class asignacion_departamento:
    def __init__(self, id_asignacion=None, id_empleado=None, id_departamento=None, fecha_asignacion=None):
        self.id_asignacion = id_asignacion
        self.id_empleado = id_empleado
        self.id_departamento = id_departamento
        self.fecha_asignacion = fecha_asignacion

    def __str__(self):
        return (f"ID asignación: {self.id_asignacion} | ID empleado: {self.id_empleado} | "
                f"ID departamento: {self.id_departamento} | fecha: {self.fecha_asignacion}")

    # ---------- CONSULTA ----------
    def obtenerTodos_asignacion_departamento(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                """SELECT ID_ASIGNACION, ID_EMPLEADO, ID_DEPARTAMENTO,
                          TO_CHAR(FECHA_ASIGNACION, 'DD-MM-YYYY')
                     FROM ASIGNACION_DEPARTAMENTO
                    ORDER BY ID_ASIGNACION"""
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de las asignaciones de departamento : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_asignacion_departamento(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO ASIGNACION_DEPARTAMENTO
                        (id_asignacion, id_empleado, id_departamento, fecha_asignacion)
                     VALUES
                        (:id, :emp, :dep, TO_DATE(:fec, 'DD-MM-YYYY'))"""
            c.cursor.execute(sql, {
                "id": self.id_asignacion,
                "emp": self.id_empleado,
                "dep": self.id_departamento,
                "fec": self.fecha_asignacion,
            })
            c.conexion.commit()
            print("¡Asignación de departamento insertada correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla asignacion_departamento : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_asignacion_departamento(self):
        c = None
        try:
            c = ConexionDB()
            sql = """UPDATE ASIGNACION_DEPARTAMENTO
                        SET id_empleado = :emp,
                            id_departamento = :dep,
                            fecha_asignacion = TO_DATE(:fec, 'DD-MM-YYYY')
                      WHERE id_asignacion = :id"""
            c.cursor.execute(sql, {
                "emp": self.id_empleado,
                "dep": self.id_departamento,
                "fec": self.fecha_asignacion,
                "id": self.id_asignacion,
            })
            c.conexion.commit()
            print("¡Asignación de departamento actualizada correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_asignacion_departamento(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            sql = """SELECT id_asignacion, id_empleado, id_departamento, fecha_asignacion
                       FROM ASIGNACION_DEPARTAMENTO
                      WHERE id_asignacion = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_asignacion = fila[0]
                self.id_empleado = fila[1]
                self.id_departamento = fila[2]
                self.fecha_asignacion = fila[3].strftime("%d-%m-%Y") if fila[3] else ""
                return True
            else:
                print("No se encontró una asignación de departamento con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar asignación de departamento por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_asignacion_departamento(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM ASIGNACION_DEPARTAMENTO WHERE id_asignacion = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe una asignación de departamento con ese ID.")
            else:
                print("¡Asignación de departamento eliminada correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
