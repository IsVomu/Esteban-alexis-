from models.conexion import ConexionDB


class registro_tiempo:
    def __init__(self, id_registro=None, fecha=None, cantidad_horas_trabajadas=None,
                 descripcion=None, id_empleado=None, id_proyecto=None):
        self.id_registro = id_registro
        self.fecha = fecha
        self.cantidad_horas_trabajadas = cantidad_horas_trabajadas
        self.descripcion = descripcion
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto

    def __str__(self):
        return (f"ID registro: {self.id_registro} | fecha: {self.fecha} | "
                f"horas: {self.cantidad_horas_trabajadas} | descripción: {self.descripcion} | "
                f"ID empleado: {self.id_empleado} | ID proyecto: {self.id_proyecto}")

    # ---------- CONSULTA ----------
    def obtenerTodos_registro_tiempo(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                """SELECT ID_REGISTRO, TO_CHAR(FECHA, 'DD-MM-YYYY'), CANTIDAD_HORAS_TRABAJADAS,
                          DESCRIPCION, ID_EMPLEADO, ID_PROYECTO
                     FROM REGISTRO_TIEMPO
                    ORDER BY ID_REGISTRO"""
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de los registros de tiempo : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_registro_tiempo(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO REGISTRO_TIEMPO
                        (id_registro, fecha, cantidad_horas_trabajadas,
                         descripcion, id_empleado, id_proyecto)
                     VALUES
                        (:id, TO_DATE(:fec, 'DD-MM-YYYY'), :horas,
                         :descr, :emp, :proy)"""
            c.cursor.execute(sql, {
                "id": self.id_registro,
                "fec": self.fecha,
                "horas": self.cantidad_horas_trabajadas,
                "descr": self.descripcion,
                "emp": self.id_empleado,
                "proy": self.id_proyecto,
            })
            c.conexion.commit()
            print("¡Registro de tiempo insertado correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla registro_tiempo : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_registro_tiempo(self):
        c = None
        try:
            c = ConexionDB()
            sql = """UPDATE REGISTRO_TIEMPO
                        SET fecha = TO_DATE(:fec, 'DD-MM-YYYY'),
                            cantidad_horas_trabajadas = :horas,
                            descripcion = :descr,
                            id_empleado = :emp,
                            id_proyecto = :proy
                      WHERE id_registro = :id"""
            c.cursor.execute(sql, {
                "fec": self.fecha,
                "horas": self.cantidad_horas_trabajadas,
                "descr": self.descripcion,
                "emp": self.id_empleado,
                "proy": self.id_proyecto,
                "id": self.id_registro,
            })
            c.conexion.commit()
            print("¡Registro de tiempo actualizado correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_registro_tiempo(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            sql = """SELECT id_registro, fecha, cantidad_horas_trabajadas,
                            descripcion, id_empleado, id_proyecto
                       FROM REGISTRO_TIEMPO
                      WHERE id_registro = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_registro = fila[0]
                self.fecha = fila[1].strftime("%d-%m-%Y") if fila[1] else ""
                self.cantidad_horas_trabajadas = float(fila[2])
                self.descripcion = fila[3]
                self.id_empleado = fila[4]
                self.id_proyecto = fila[5]
                return True
            else:
                print("No se encontró un registro de tiempo con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar registro de tiempo por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_registro_tiempo(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM REGISTRO_TIEMPO WHERE id_registro = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe un registro de tiempo con ese ID.")
            else:
                print("¡Registro de tiempo eliminado correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
