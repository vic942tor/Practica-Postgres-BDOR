from conexion import conectar_db
from psycopg2 import (
    IntegrityError,
    ProgrammingError,
    OperationalError,
    DatabaseError
)

def crear_esquema():
    # Intentamos obtener la conexión desde el módulo externo
    conn = conectar_db()
    if not conn:
        print("No se pudo establecer conexión con la base de datos.")
        return

    try:
        # Creamos el cursor para ejecutar las sentencias
        cur = conn.cursor()

        # Creación de Tipos Compuestos
        cur.execute("""
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'artist_type') THEN
                    CREATE TYPE artist_type AS (
                        nombre VARCHAR(50),
                        apellido VARCHAR(50),
                        nacionalidad VARCHAR(50)
                    );
                END IF;
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sale_info') THEN
                    CREATE TYPE sale_info AS (
                        customer_name VARCHAR(100),
                        sale_date DATE,
                        discos_comprados INTEGER[]
                    );
                END IF;
            END $$;
        """)

        # Creación de Tablas
        cur.execute("""
            CREATE TABLE IF NOT EXISTS artistas (
                id_artista SERIAL PRIMARY KEY,
                info artist_type
            );

            CREATE TABLE IF NOT EXISTS discos (
                id_disco SERIAL PRIMARY KEY,
                titulo VARCHAR(100),
                lanzamiento INTEGER,
                generos TEXT[],
                artistas_ids INTEGER[]
            );

            CREATE TABLE IF NOT EXISTS ventas (
                id_venta SERIAL PRIMARY KEY,
                detalle sale_info
            );
        """)

        # Confirmamos los cambios en la base de datos
        conn.commit()
        print("Tablas y tipos creados con éxito.")

    # Manejo de excepciones específicas de psycopg2
    except IntegrityError as e:
        conn.rollback()
        print("Error de integridad:", e)
    except ProgrammingError as e:
        conn.rollback()
        print("Error de sintaxis SQL:", e)
    except (OperationalError, DatabaseError) as e:
        conn.rollback()
        print("Error de base de datos:", e)

    # Cierre de recursos
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    crear_esquema()