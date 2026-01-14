import pytest
import datetime
from conexion import conectar_db
from CRUDyTransacciones import alta_venta_completa, consultas_obligatorias

def preparar_bd_pruebas():
    """
    Deja la base de datos en un estado controlado para evitar que los test 
    puedan fallar por cambios futuros en la BD real.
    """
    conn = conectar_db()
    # assert comprueba que algo sea verdad. Si es None, el test se detiene aquí.
    assert conn is not None

    with conn.cursor() as cur:
        # Borra datos, reinicia contadores (IDs a 1) y borra en cascada.
        cur.execute("TRUNCATE ventas, discos, artistas RESTART IDENTITY CASCADE;")

        # Datos de prueba: Insertamos artistas base para que los discos tengan a quién referenciar.
        cur.execute(
            "INSERT INTO artistas (info) VALUES (('Aimer', 'Desconocido', 'Japonesa'))"
        )
        cur.execute(
            "INSERT INTO artistas (info) VALUES (('Vaundy', 'Desconocido', 'Japonesa'))"
        )

        # Insertamos un disco. Usamos %s para inyectar los datos de forma segura.
        cur.execute("""
            INSERT INTO discos (titulo, lanzamiento, generos, artistas_ids)
            VALUES (%s, %s, %s, %s)
        """, ("Deep Down", 2022, ["Pop", "Anime", "Rock"], [1])
        )

    # Confirmamos cambios y cerramos para dejar la base lista para los tests.
    conn.commit()
    conn.close()

# BLOQUE DE TESTS

def test_conexion():
    """Prueba básica: ¿La función conectar_db realmente devuelve una conexión?"""
    conn = conectar_db()
    assert conn is not None
    conn.close()


def test_alta_venta_y_commit():
    """Prueba de éxito: Al insertar datos correctos, el contador en la BD debe subir a 1."""
    preparar_bd_pruebas() # Reset de la base de datos
    conn = conectar_db()

    try:
        # Ejecutamos la lógica de inserción de ventas
        alta_venta_completa(
            conn,
            "VíctorTest",
            str(datetime.date.today()), 
            [1] # ID del disco insertado en el setup
        )

        with conn.cursor() as cur:
            # Verificamos si el nombre existe en el tipo compuesto 'detalle'
            cur.execute(
                "SELECT COUNT(*) FROM ventas WHERE (detalle).customer_name = %s",
                ("VíctorTest",)
            )
            # El test es exitoso si el resultado de la cuenta es exactamente 1
            assert cur.fetchone()[0] == 1
    finally:
        conn.close()


def test_rollback_venta_vacia():
    """Prueba de fallo: Si intentamos una venta sin discos, el sistema NO debe guardar nada."""
    preparar_bd_pruebas()
    conn = conectar_db()

    try:
        # Forzamos el error enviando una lista de discos vacía []
        alta_venta_completa(
            conn,
            "Cliente Fallido",
            "2025-01-01",
            []
        )

        with conn.cursor() as cur:
            # Comprobamos que el cliente NO se guardó.
            cur.execute(
                "SELECT COUNT(*) FROM ventas WHERE (detalle).customer_name = %s",
                ("Cliente Fallido",)
            )
            # El test es exitoso si la cuenta es 0 (rollback funcionó)
            assert cur.fetchone()[0] == 0
    finally:
        conn.close()


def test_consultas_bdor():
    """Prueba de compatibilidad: Verifica que las consultas complejas (Arrays/Tipos) no fallan."""
    preparar_bd_pruebas()
    conn = conectar_db()

    try:
        # Solo comprobamos que la función de lectura se ejecute sin lanzar excepciones SQL
        consultas_obligatorias(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    import pytest

    # Ejecuta pytest sobre este mismo archivo en modo verbose (No había manera de que me detectara el pytest en en path
    # con esto puedes ejecutar los test directamente ejecutando el archivo normal como cualquier otro .py)
    sys.exit(pytest.main([__file__, "-v"]))
