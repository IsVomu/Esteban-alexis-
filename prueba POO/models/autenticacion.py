import hashlib

from models.conexion import ConexionDB


class autenticacion:
    def __init__(self, id_autenticacion=None, id_empleado=None, solo_usuario=None, contrasena=None):
        self.id_autenticacion = id_autenticacion
        self.id_empleado = id_empleado
        self.solo_usuario = solo_usuario
        self.contrasena = contrasena    
        self.contrasena_hash = None        

    def __str__(self):
        return (f"ID autenticación: {self.id_autenticacion} | ID empleado: {self.id_empleado} | "
                f"usuario: {self.solo_usuario}")

    @staticmethod
    def _hashear(texto):
        return hashlib.sha256(texto.encode("utf-8")).hexdigest().upper()

    # ---------- VALIDAR USUARIO (LOGIN) ----------
    def validarUsuario(self, usuario, contrasena):
        self.id_autenticacion = None
        self.id_empleado = None
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                """SELECT id_autenticacion, id_empleado, solo_usuario, contrasena_hash
                     FROM AUTENTICACION
                    WHERE LOWER(solo_usuario) = LOWER(:usu)""",
                {"usu": usuario}
            )
            fila = c.cursor.fetchone()
            if not fila:
                return "no_existe"

            self.id_autenticacion = fila[0]
            self.id_empleado = fila[1]
            self.solo_usuario = fila[2]
            self.contrasena_hash = fila[3]

            if self._hashear(contrasena) == fila[3]:
                return "ok"
            return "clave_incorrecta"
        except Exception as e:
            print(f"ERROR al validar el usuario : {e}")
            return "error"
        finally:
            if c:
                c.cerrar()

    # ---------- CONSULTA ----------
    def obtenerTodos_autenticacion(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                """SELECT ID_AUTENTICACION, ID_EMPLEADO, SOLO_USUARIO
                     FROM AUTENTICACION
                    ORDER BY ID_AUTENTICACION"""
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de autenticación : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_autenticacion(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO AUTENTICACION
                        (id_autenticacion, id_empleado, solo_usuario, contrasena_hash)
                     VALUES
                        (:id, :emp, :usu, :hash)"""
            c.cursor.execute(sql, {
                "id": self.id_autenticacion,
                "emp": self.id_empleado,
                "usu": self.solo_usuario,
                "hash": self._hashear(self.contrasena),
            })
            c.conexion.commit()
            print("¡Autenticación insertada correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla autenticacion : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_autenticacion(self):
        c = None
        try:
            c = ConexionDB()
            if self.contrasena:
                self.contrasena_hash = self._hashear(self.contrasena)

            sql = """UPDATE AUTENTICACION
                        SET id_empleado = :emp,
                            solo_usuario = :usu,
                            contrasena_hash = :hash
                      WHERE id_autenticacion = :id"""
            c.cursor.execute(sql, {
                "emp": self.id_empleado,
                "usu": self.solo_usuario,
                "hash": self.contrasena_hash,
                "id": self.id_autenticacion,
            })
            c.conexion.commit()
            print("¡Autenticación actualizada correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_autenticacion(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            sql = """SELECT id_autenticacion, id_empleado, solo_usuario, contrasena_hash
                       FROM AUTENTICACION
                      WHERE id_autenticacion = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_autenticacion = fila[0]
                self.id_empleado = fila[1]
                self.solo_usuario = fila[2]
                self.contrasena_hash = fila[3]
                self.contrasena = None
                return True
            else:
                print("No se encontró una autenticación con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar autenticación por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_autenticacion(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM AUTENTICACION WHERE id_autenticacion = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe una autenticación con ese ID.")
            else:
                print("¡Autenticación eliminada correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
