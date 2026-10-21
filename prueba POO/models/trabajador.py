from models.conexion import ConexionDB


class trabajador:
    def __init__(self, id_empleado=None, nombre=None, direccion=None, numero_telefono=None,
                 correo_electronico=None, inicio_contrato=None, salario=None, id_departamento=None):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.direccion = direccion
        self.numero_telefono = numero_telefono
        self.correo_electronico = correo_electronico
        self.inicio_contrato = inicio_contrato
        self.salario = salario
        self.id_departamento = id_departamento

    def __str__(self):
        return (f"ID: {self.id_empleado} | nombre: {self.nombre} | dirección: {self.direccion} | "
                f"teléfono: {self.numero_telefono} | correo: {self.correo_electronico} | "
                f"inicio de contrato: {self.inicio_contrato} | salario: {self.salario} | "
                f"ID departamento: {self.id_departamento}")

    # ---------- CONSULTA ----------
    def obtenerTodos_trabajador(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                """SELECT ID_EMPLEADO, NOMBRE, DIRECCION, NUMERO_TELEFONO, CORREO_ELECTRONICO,
                          TO_CHAR(INICIO_CONTRATO, 'DD-MM-YYYY'), SALARIO, ID_DEPARTAMENTO
                     FROM TRABAJADOR
                    ORDER BY ID_EMPLEADO"""
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de los trabajadores : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_trabajador(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO TRABAJADOR
                        (id_empleado, nombre, direccion, numero_telefono, correo_electronico,
                         inicio_contrato, salario, id_departamento)
                     VALUES
                        (:id, :nom, :dir, :tel, :correo,
                         TO_DATE(:fec, 'DD-MM-YYYY'), :salario, :dep)"""
            c.cursor.execute(sql, {
                "id": self.id_empleado,
                "nom": self.nombre,
                "dir": self.direccion,
                "tel": self.numero_telefono,
                "correo": self.correo_electronico,
                "fec": self.inicio_contrato,
                "salario": self.salario,
                "dep": self.id_departamento,
            })
            c.conexion.commit()
            print("¡Trabajador insertado correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla trabajador : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_trabajador(self):
        c = None
        try:
            c = ConexionDB()
            sql = """UPDATE TRABAJADOR
                        SET nombre = :nom,
                            direccion = :dir,
                            numero_telefono = :tel,
                            correo_electronico = :correo,
                            inicio_contrato = TO_DATE(:fec, 'DD-MM-YYYY'),
                            salario = :salario,
                            id_departamento = :dep
                      WHERE id_empleado = :id"""
            c.cursor.execute(sql, {
                "nom": self.nombre,
                "dir": self.direccion,
                "tel": self.numero_telefono,
                "correo": self.correo_electronico,
                "fec": self.inicio_contrato,
                "salario": self.salario,
                "dep": self.id_departamento,
                "id": self.id_empleado,
            })
            c.conexion.commit()
            print("¡Trabajador actualizado correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_trabajador(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            sql = """SELECT id_empleado, nombre, direccion, numero_telefono, correo_electronico,
                            inicio_contrato, salario, id_departamento
                       FROM TRABAJADOR
                      WHERE id_empleado = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_empleado = fila[0]
                self.nombre = fila[1]
                self.direccion = fila[2]
                self.numero_telefono = fila[3]
                self.correo_electronico = fila[4]
                self.inicio_contrato = fila[5].strftime("%d-%m-%Y") if fila[5] else ""
                self.salario = int(fila[6])
                self.id_departamento = fila[7]
                return True
            else:
                print("No se encontró un trabajador con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar trabajador por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_trabajador(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM TRABAJADOR WHERE id_empleado = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe un trabajador con ese ID.")
            else:
                print("¡Trabajador eliminado correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
