import oracledb

class ConexionDB:
    
    def __init__(self):
        try:
            self.conexion = oracledb.connect(
            user = "PRUEBA",
            password = "inacap",
            host = "localhost",
            port = 1521,
            service_name = "xe"
            )
            self.cursor = self.conexion.cursor()
            print("CONEXION ESTABLECIDA")
        except Exception as e:
            print(f"ERROR NO SE PUDO ESTABLECER A LA CONEXION {e}")
            raise
        
    def cerrar(self):
        try:
            if self.cursor:
                self.cursor.close()
        except Exception:
            pass
        try:
            if self.conexion:
                self.conexion.close()
        except Exception:
            pass
            