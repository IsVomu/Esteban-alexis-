from models.conexion import ConexionDB


class departamento:
    def __init__(self, id_departamento=None, nombre=None, gerente_asociado=None):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.gerente_asociado = gerente_asociado

    def __str__(self):
        return (f"ID de departamento: {self.id_departamento} | "
                f"nombre de departamento: {self.nombre} | "
                f"gerente asociado: {self.gerente_asociado}")

    # ---------- CONSULTA ----------
    def obtenerTodos_departamento(self):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "SELECT ID_DEPARTAMENTO, NOMBRE, GERENTE_ASOCIADO FROM DEPARTAMENTO ORDER BY ID_DEPARTAMENTO"
            )
            return c.cursor.fetchall()
        except Exception as e:
            print(f"ERROR al obtener datos de los departamentos : {e}")
            return []
        finally:
            if c:
                c.cerrar()

    # ---------- INSERTAR ----------
    def insertar_departamento(self):
        c = None
        try:
            c = ConexionDB()
            sql = """INSERT INTO DEPARTAMENTO
                        (id_departamento, nombre, gerente_asociado)
                     VALUES
                        (:id, :nom, :gere_aso)"""
            c.cursor.execute(sql, {
                "id": self.id_departamento,
                "nom": self.nombre,
                "gere_aso": self.gerente_asociado,
            })
            c.conexion.commit()
            print("¡Departamento insertado correctamente!")
        except Exception as e:
            print(f"ERROR al insertar datos en la tabla departamento : {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- ACTUALIZAR ----------
    def actualizar_departamento(self):
        c = None
        try:
            c = ConexionDB()
            # Antes faltaban el "=" y la coma en gerente_asociado, el parámetro
            # :gere_aso no existía en el SQL y el WHERE usaba la columna "id".
            sql = """UPDATE DEPARTAMENTO
                        SET nombre = :nom,
                            gerente_asociado = :gere_aso
                      WHERE id_departamento = :id"""
            c.cursor.execute(sql, {
                "nom": self.nombre,
                "gere_aso": self.gerente_asociado,
                "id": self.id_departamento,
            })
            c.conexion.commit()
            print("¡Departamento actualizado correctamente!")
        except Exception as e:
            print(f"ERROR al actualizar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()

    # ---------- CARGAR POR ID ----------
    def cargarPorID_departamento(self, idBuscando):
        c = None
        try:
            c = ConexionDB()
            # Antes el WHERE usaba "id", pero la columna se llama id_departamento
            sql = """SELECT id_departamento, nombre, gerente_asociado
                       FROM DEPARTAMENTO
                      WHERE id_departamento = :id"""
            c.cursor.execute(sql, {"id": idBuscando})
            fila = c.cursor.fetchone()

            if fila:
                self.id_departamento = fila[0]
                self.nombre = fila[1]
                self.gerente_asociado = fila[2]   # antes decía self.gerente_asociado[2]
                return True
            else:
                print("No se encontró un departamento con ese ID.")
                return False
        except Exception as e:
            print(f"ERROR al cargar departamento por ID: {e}")
            return False
        finally:
            if c:
                c.cerrar()

    # ---------- ELIMINAR ----------
    def eliminar_departamento(self, idEliminar):
        c = None
        try:
            c = ConexionDB()
            c.cursor.execute(
                "DELETE FROM DEPARTAMENTO WHERE id_departamento = :id",
                {"id": idEliminar}
            )
            filas = c.cursor.rowcount
            c.conexion.commit()
            if filas == 0:
                print("No existe un departamento con ese ID.")
            else:
                print("¡Departamento eliminado correctamente!")
        except Exception as e:
            print(f"ERROR al eliminar en la Base de Datos: {e}")
        finally:
            if c:
                c.cerrar()
