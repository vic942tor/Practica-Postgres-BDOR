from conexion import conectar_db
from psycopg2 import DatabaseError

def insertar_datos_ejemplo():
    conn = conectar_db()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            print("Insertando datos de ejemplo...")

            # Insertar Artistas (Tipo Compuesto: nombre, apellido, nacionalidad)
            # Usamos la sintaxis de tuplas de Python que psycopg2 traduce a (nombre ,apellido ,nacionalidad)
            artistas = [
                ("Aimer", "chen", "Chino"),
                ("David", "Gonzalez", "Portugues"),
                ("Antonio", "Gutierrez", "Español"),
                ("Hironobu", "Kageyama", "Japonesa")
            ]
            
            for art in artistas:
                cur.execute(
                    "INSERT INTO artistas (info) VALUES ((%s, %s, %s))",
                    art
                )
            # Insertar Discos Arrays de géneros e IDs de artistas
            # El ID 1 será Aimer, el ID 2 David, etc.
            discos = [
                ("Deep Down", 2022, ["Pop", "Anime", "Rock"], [1]),
                ("Chainsaw Blood", 2022, ["Rock", "J-Pop"], [2]),
                ("KICK BACK", 2022, ["K-Pop", "Rock"], [3]),
                ("Cha-La Head-Cha-La", 1989, ["Anisong", "Classic"], [4])
            ]

            for disco in discos:
                cur.execute(
                    "INSERT INTO discos (titulo, lanzamiento, generos, artistas_ids) VALUES (%s, %s, %s, %s)",
                    disco
                )

            # Insertar una Venta inicial (Tipo Compuesto con Array dentro)
            # (customer_name, sale_date, discos_comprados_ids[])
            cur.execute(
                "INSERT INTO ventas (detalle) VALUES ((%s, %s, %s))",
                ("Juan Pérez", "2025-01-15", [1, 2])
            )

            conn.commit()
            print("¡Datos insertados correctamente!")

    except DatabaseError as e:
        conn.rollback()
        print(f"Error al poblar datos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    insertar_datos_ejemplo()