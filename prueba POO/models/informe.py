from models.conexion import ConexionDB


class informe:
    def __init__(self, id_informe=None, informacion_empleado=None, proyectos=None,
                 departamento=None, registro_de_tiempo=None, fecha_generacion=None,
                 id_administrador=None):
        self.id_informe = id_informe
        self.informacion_empleado = informacion_empleado
        self.proyectos = proyectos
        self.departamento = departamento
        self.registro_de_tiempo = registro_de_tiempo
        self.fecha_generacion = fecha_generacion
        self.id_administrador = id_administrador

    def __str__(self):
        return (f"ID informe: {self.id_informe} | empleado: {self.informacion_empleado} | "
                f"proyectos: {self.proyectos} | departamento: {self.departamento} | "
                f"tiempo: {self.registro_de_tiempo} | fecha: {self.fecha_generacion} | "
                f"ID administrador: {self.id_administrador}")

    # ---------- CONSULTA ----------
    def obtenerTodos_informe(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                """SELECT ID_INFORME, INFORMACION_EMPLEADO, PROYECTOS, DEPARTAMENTO,
                          REGISTRO_DE_TIEMPO, TO_CHAR(FECHA_GENERACION, 'DD-MM-YYYY'),
                          ID_ADMINISTRADOR
                     FROM INFORME
                    ORDER BY ID_INFORME"""
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de los informes : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_informe(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO INFORME
                        (id_informe, informacion_empleado, proyectos, departamento,
                         registro_de_tiempo, fecha_generacion, id_administrador)
                     VALUES
                        (:id, :info, :proy, :dep, :tiempo,
                         TO_DATE(:fec, 'DD-MM-YYYY'), :admin)"""
            c.cursor.execute(sql, {
                "id": self.id_informe,
                "info": self.informacion_empleado,
                "proy": self.proyectos,
                "dep": self.departamento,
                "tiempo": self.registro_de_tiempo,
                "fec": self.fecha_generacion,
                "admin": self.id_administrador,
            })
            c.conexion.commit()
            print("¡Informe insertado correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla informe : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_informe(self):
        c = None
        try:
            c = ConexionDB()
            sql = """UPDATE INFORME
                        SET informacion_empleado = :info,
                            proyectos = :proy,
                            departamento = :dep,
                            registro_de_tiempo = :tiempo,
                            fecha_generacion = TO_DATE(:fec, 'DD-MM-YYYY'),
                            id_administrador = :admin
                      WHERE id_informe = :id"""
            c.cursor.execute(sql, {
                "info": self.informacion_empleado,
                "proy": self.proyectos,
                "dep": self.departamento,
                "tiempo": self.registro_de_tiempo,
                "fec": self.fecha_generacion,
                "admin": self.id_administrador,
                "id": self.id_informe,
            })
            c.conexion.commit()
            print("¡Informe actualizado correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_informe(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            sql = """SELECT id_informe, informacion_empleado, proyectos, departamento,
                            registro_de_tiempo, fecha_generacion, id_administrador
                       FROM INFORME
                      WHERE id_informe = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_informe = fila[0]
                self.informacion_empleado = fila[1]
                self.proyectos = fila[2]
                self.departamento = fila[3]
                self.registro_de_tiempo = fila[4]
                self.fecha_generacion = fila[5].strftime("%d-%m-%Y") if fila[5] else ""
                self.id_administrador = fila[6]
                return True
            else:
                print("No se encontró un informe con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar informe por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_informe(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM INFORME WHERE id_informe = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe un informe con ese ID.")
            else:
                print("¡Informe eliminado correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
