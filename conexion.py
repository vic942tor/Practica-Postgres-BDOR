import psycopg2
from psycopg2 import OperationalError

def conectar_db():
    """
    Establece una conexión con la base de datos PostgreSQL.
    Retorna el objeto de conexión si tiene éxito, o None si hay un error.
    """
    try:
        conexion = psycopg2.connect(
            host="localhost",      # Dirección  
            dbname="aed_db",       # Nombre de la BD
            user="aed_user",       # Usuario 
            password="aed_pass",   # Contraseña 
            port=5432              # Puerto 
        )
        return conexion
        
    except OperationalError as e:
        print(f"Error de conexión: {e}")
        return None