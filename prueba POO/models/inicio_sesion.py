from models.conexion import ConexionDB


class inicio_sesion:

    def __init__(self, id_sesion=None, id_autenticacion=None, correo=None,
                 fecha_hora=None, exitoso=None):
        self.id_sesion = id_sesion
        self.id_autenticacion = id_autenticacion
        self.correo = correo
        self.fecha_hora = fecha_hora
        self.exitoso = exitoso

    def __str__(self):
        return (f"ID sesión: {self.id_sesion} | ID autenticación: {self.id_autenticacion} | "
                f"correo: {self.correo} | fecha y hora: {self.fecha_hora} | exitoso: {self.exitoso}")

    # ---------- CONSULTA ----------
    def obtenerTodos_inicio_sesion(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                """SELECT ID_SESION, ID_AUTENTICACION, CORREO,
                          TO_CHAR(FECHA_HORA, 'DD-MM-YYYY HH24:MI'), EXITOSO
                     FROM INICIO_SESION
                    ORDER BY ID_SESION"""
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de los inicios de sesión : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_inicio_sesion(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO INICIO_SESION
                        (id_sesion, id_autenticacion, correo, fecha_hora, exitoso)
                     VALUES
                        (:id, :aut, :correo, TO_TIMESTAMP(:fec, 'DD-MM-YYYY HH24:MI'), :exito)"""
            c.cursor.execute(sql, {
                "id": self.id_sesion,
                "aut": self.id_autenticacion,
                "correo": self.correo,
                "fec": self.fecha_hora,
                "exito": self.exitoso,
            })
            c.conexion.commit()
            print("¡Inicio de sesión insertado correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla inicio_sesion : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_inicio_sesion(self):
        c = None
        try:
            c = ConexionDB()
            sql = """UPDATE INICIO_SESION
                        SET id_autenticacion = :aut,
                            correo = :correo,
                            fecha_hora = TO_TIMESTAMP(:fec, 'DD-MM-YYYY HH24:MI'),
                            exitoso = :exito
                      WHERE id_sesion = :id"""
            c.cursor.execute(sql, {
                "aut": self.id_autenticacion,
                "correo": self.correo,
                "fec": self.fecha_hora,
                "exito": self.exitoso,
                "id": self.id_sesion,
            })
            c.conexion.commit()
            print("¡Inicio de sesión actualizado correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_inicio_sesion(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            sql = """SELECT id_sesion, id_autenticacion, correo, fecha_hora, exitoso
                       FROM INICIO_SESION
                      WHERE id_sesion = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_sesion = fila[0]
                self.id_autenticacion = fila[1]
                self.correo = fila[2]
                self.fecha_hora = fila[3].strftime("%d-%m-%Y %H:%M") if fila[3] else ""
                self.exitoso = fila[4]
                return True
            else:
                print("No se encontró un inicio de sesión con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar inicio de sesión por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_inicio_sesion(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM INICIO_SESION WHERE id_sesion = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe un inicio de sesión con ese ID.")
            else:
                print("¡Inicio de sesión eliminado correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
