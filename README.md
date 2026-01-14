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
- **Arrays**: Uso de `TEXT[]` para géneros y `INTEGER[]` para relaciones entre discos y artistas.
- **Operadores Especiales**: Uso de `ANY` y `unnest()` para realizar búsquedas eficientes dentro de colecciones.

## Transacciones y Seguridad
- **Atomicidad**: Cada operación CRUD está protegida por un bloque `try-except`.
- **Commit/Rollback**: Se demuestra el uso de `conn.commit()` para ventas exitosas y `conn.rollback()` para revertir cambios ante errores de validación o integridad.
- **Prevención de Inyección SQL**: Todas las consultas utilizan **marcadores de posición (%s)** para separar la lógica del motor de los datos del usuario.

## Pruebas Automatizadas (Pytest)
Se han incluido tests para verificar:
1. Conexión estable con el servidor.
2. Inserción correcta con persistencia de datos.
3. Funcionamiento del Rollback ante fallos lógicos.
4. Compatibilidad de las consultas complejas sobre tipos y arrays.

Para ejecutar los tests: `python test_pruebas.py` en la terminal o ejecutandolo desde el propio IDE con el botón "RUN/START".

## Análisis Técnico del Modelo BDOR
Basándomeen lo experimentado esta actividad, se extraen las siguientes conclusiones sobre la comparativa entre el modelo **Objeto-Relacional** y los modelos tradicionales:

* **Ventajas de la implementación**:
    * **Estructura Natural**: El uso de `Arrays` permite una estructura más compacta, eliminando la necesidad de tablas de unión (N:M) adicionales para los géneros musicales.
    * **Encapsulamiento de Datos**: Los tipos compuestos permiten tratar entidades relacionadas como una sola unidad, simplificando la lógica de inserción en la tabla de artistas.
* **Inconvenientes Detectados**:
    * **Sintaxis Específica**: Acceder a campos internos de un tipo compuesto requiere una sintaxis de paréntesis y punto `(columna).atributo`, lo que aumenta la complejidad del SQL.
    * **Dependencia del Motor**: La solución es dependiente de PostgreSQL, ya que los tipos compuestos y el manejo de arrays varían significativamente en otros sistemas gestores por lo que la portabilidad no es una opción vialble.

## Explicación de Transacciones (Control de Integridad)
Para garantizar la fiabilidad del sistema, se ha implementado un control de transacciones:

1. **Caso de Éxito (Commit)**: Cuando la venta es válida, se ejecuta `conn.commit()` para persistir los cambios permanentemente.
2. **Caso de Error (Rollback)**: Si ocurre un fallo (como una venta sin discos), se ejecuta `conn.rollback()` para revertir cualquier operación parcial, asegurando que la base de datos no quede en un estado inconsistente. Este comportamiento se verifica específicamente en el test `test_rollback_venta_vacia`.
