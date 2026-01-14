# Gestión de Tienda de Música - Modelo BDOR (PostgreSQL + Python)

Este proyecto desarrolla una solución para la gestión de un catálogo musical utilizando una base de datos **Objeto-Relacional**. Se implementa bajo un entorno Dockerizado y se gestiona mediante Python 3.13.

## Configuración e Instalación
1. **Entorno Docker**:
   - Red: `docker network create AED`
   - Contenedor: `postgres-aed` (Puerto 5432)
2. **Dependencias**: `pip install psycopg2 pytest`

## Características BDOR Implementadas
Se han utilizado las capacidades extendidas de PostgreSQL para cumplir con el enunciado:
- **Tipos Compuestos**: 
  - `artist_type`: Encapsula nombre, apellido y nacionalidad.
  - `sale_info`: Agrupa cliente, fecha y un array de productos.
- **Arrays**: Uso de `TEXT[]` para géneros y `INTEGER[]` para relaciones.
- **Operadores Especiales**: Uso de `ANY` y `unnest()` para realizar búsquedas eficientes dentro de colecciones.

## Transacciones y Seguridad
- **Atomicidad**: Cada operación CRUD está protegida por un bloque `try-except`.
- **Commit/Rollback**: Se demuestra el uso de `conn.commit()` para ventas exitosas y `conn.rollback()` para revertir cambios ante errores de validación (ej: ventas sin discos).
- **Prevención de Inyección SQL**: Todas las consultas utilizan **marcadores de posición (%s)** para separar la lógica del motor de los datos del usuario.

## Pruebas Automatizadas (Pytest)
Se han incluido tests para verificar:
1. Conexión estable con el servidor.
2. Inserción correcta con persistencia de datos.
3. Funcionamiento del Rollback ante fallos lógicos.
4. Compatibilidad de las consultas complejas sobre tipos y arrays.

Para ejecutar los tests: `python test_pruebas.py` en la terminal, o simplemente pulsar el botón de "Run/Play" desde tu IDE
