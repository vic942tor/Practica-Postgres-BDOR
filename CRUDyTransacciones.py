from conexion import conectar_db
from psycopg2 import IntegrityError, ProgrammingError, OperationalError, DatabaseError


# CREATE
def alta_venta_completa(conn, nombre_cliente, fecha, lista_discos):
    try:
        # Si no hay discos, no tiene sentido seguir y lanzamos un error
        if not lista_discos:
            raise ValueError("No hay discos para la venta.")

        # 'with conn.cursor()' crea un cursor que luego se cierra al ternimar
        with conn.cursor() as cur:
            # Preparamos la orden SQL. Los %s son huecos seguros (para mejorar la seguridad de la BD)
            sql = "INSERT INTO ventas (detalle) VALUES ((%s, %s, %s))"
            # El cursor rellena los %s con nuestros datos reales y envía la orden
            cur.execute(sql, (nombre_cliente, fecha, lista_discos))

        #Los cambios no son permanentes hasta que hacemos 'commit'
        conn.commit()
        print(f"Venta de {nombre_cliente} registrada con éxito.")

    except ValueError as e:
        print("Error de validación:", e)

    except IntegrityError as e:
        conn.rollback()
        print("Error de integridad:", e)

    except (ProgrammingError, OperationalError) as e:
        conn.rollback()
        print("Error de la base de datos:", e)

    except DatabaseError as e:
        conn.rollback()
        print("Error general de la base de datos:", e)


# UPDATE
def actualizar_disco_generos(conn, id_disco, nuevos_generos):
    try:
        with conn.cursor() as cur:
            # Pedimos a la DB que actualice los géneros de un disco específico por su ID
            cur.execute(
                "UPDATE discos SET generos = %s WHERE id_disco = %s",
                (nuevos_generos, id_disco)
            )

            # 'rowcount' nos dice a cuántas filas ha afectado la orden. Si es 0, el ID no existía.
            if cur.rowcount == 0:
                raise LookupError(f"No existe el disco con id {id_disco}")

        conn.commit()
        print("Géneros del disco actualizados.")
        
    except LookupError as e:
        conn.rollback()
        print("Error de búsqueda:", e)

    except IntegrityError as e:
        conn.rollback()
        print("Error de integridad:", e)

    except DatabaseError as e:
        conn.rollback()
        print("Error de base de datos:", e)


# DELETE
def eliminar_artista(conn, id_artista):
    try:
        with conn.cursor() as cur:
            # El ID se pasa como una tupla
            cur.execute(
                "DELETE FROM artistas WHERE id_artista = %s",
                (id_artista,)
            )
            # Comprobamos si realmente se borró algo
            if cur.rowcount == 0:
                raise LookupError(f"No existe el artista con id {id_artista}")
                
        conn.commit()
        print(f"Artista {id_artista} eliminado.")

    except LookupError as e:
        conn.rollback()
        print("Error:", e)

    except IntegrityError as e:
        conn.rollback()
        print("Error de integridad (posible dependencia):", e)

    except DatabaseError as e:
        conn.rollback()
        print("Error de base de datos:", e)

def consultas_obligatorias(conn):
    try:
        with conn.cursor() as cur:
            # 1. ¿Qué discos incluyen un género específico? (Usa operador ANY para el Array)
            cur.execute("SELECT titulo FROM discos WHERE 'Rock' = ANY(generos)")
            print("Discos de Rock:", cur.fetchall())

            # 2. ¿Qué discos ha comprado un cliente determinado? (Acceso al Tipo Compuesto)
            cur.execute("SELECT (detalle).discos_comprados FROM ventas WHERE (detalle).customer_name = %s", ("Juan Pérez",))
            print("Discos comprados por Juan Pérez:", cur.fetchone())

            # 3. Artistas que han colaborado en un disco (Ej: ID 1)
            # unnest() convierte el array {1,2,3} en filas para que ANY pueda compararlas
            cur.execute("""
                SELECT (info).nombre, (info).nacionalidad FROM artistas 
                WHERE id_artista = ANY (
                    SELECT unnest(artistas_ids) FROM discos WHERE id_disco = %s
                )
            """, (1,))
            print("Artistas del disco 1:", cur.fetchall())
    except DatabaseError as e:
        print("Error en consultas:", e)

# MAIN
if __name__ == "__main__":
    conn = conectar_db()
    if not conn:
        print("No se pudo conectar a la base de datos.")
    else:
        try:
            # Operaciones de escritura (CREATE / UPDATE / DELETE)
            alta_venta_completa(conn, "Juan Pérez", "2025-01-15", [1, 2, 3])
            actualizar_disco_generos(conn, 1, ["Rock", "Indie"])
            eliminar_artista(conn, 1)

            # Consultas obligatorias
            consultas_obligatorias(conn)

        finally:
            # Cerramos la conexión una sola vez al final
            conn.close()