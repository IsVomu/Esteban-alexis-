from models.conexion import ConexionDB


class proyecto:
    def __init__(self, id_proyecto=None, nombre=None, descripcion=None, fecha_inicio=None):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio

    def __str__(self):
        return (f"ID proyecto: {self.id_proyecto} | nombre: {self.nombre} | "
                f"descripción: {self.descripcion} | fecha de inicio: {self.fecha_inicio}")

    # ---------- CONSULTA ----------
    def obtenerTodos_proyecto(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                """SELECT ID_PROYECTO, NOMBRE, DESCRIPCION,
                          TO_CHAR(FECHA_INICIO, 'DD-MM-YYYY')
                     FROM PROYECTO
                    ORDER BY ID_PROYECTO"""
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de los proyectos : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_proyecto(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO PROYECTO
                        (id_proyecto, nombre, descripcion, fecha_inicio)
                     VALUES
                        (:id, :nom, :descr, TO_DATE(:fec, 'DD-MM-YYYY'))"""
            c.cursor.execute(sql, {
                "id": self.id_proyecto,
                "nom": self.nombre,
                "descr": self.descripcion,
                "fec": self.fecha_inicio,
            })
            c.conexion.commit()
            print("¡Proyecto insertado correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla proyecto : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_proyecto(self):
        c = None
        try:
            c = ConexionDB()
            sql = """UPDATE PROYECTO
                        SET nombre = :nom,
                            descripcion = :descr,
                            fecha_inicio = TO_DATE(:fec, 'DD-MM-YYYY')
                      WHERE id_proyecto = :id"""
            c.cursor.execute(sql, {
                "nom": self.nombre,
                "descr": self.descripcion,
                "fec": self.fecha_inicio,
                "id": self.id_proyecto,
            })
            c.conexion.commit()
            print("¡Proyecto actualizado correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_proyecto(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            sql = """SELECT id_proyecto, nombre, descripcion, fecha_inicio
                       FROM PROYECTO
                      WHERE id_proyecto = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_proyecto = fila[0]
                self.nombre = fila[1]
                self.descripcion = fila[2]
                self.fecha_inicio = fila[3].strftime("%d-%m-%Y") if fila[3] else ""
                return True
            else:
                print("No se encontró un proyecto con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar proyecto por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_proyecto(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM PROYECTO WHERE id_proyecto = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe un proyecto con ese ID.")
            else:
                print("¡Proyecto eliminado correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
