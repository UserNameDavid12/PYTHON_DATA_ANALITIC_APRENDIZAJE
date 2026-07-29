# ============================================================
# db.py - Capa de acceso a datos (Data Access Layer)
# ============================================================
import psycopg2
from typing import List, Optional, Tuple

# ------------------------------------------------------------
# Configuración de la conexión (cambia la contraseña por la tuya)
# ------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "inventario_db",
    "user": "postgres",
    "password": "1234"   # <--- CAMBIA AQUÍ
}

def get_connection():
    """Devuelve una conexión a la base de datos."""
    return psycopg2.connect(**DB_CONFIG)

# ------------------------------------------------------------
# Operaciones CRUD básicas (para reutilizar luego en Inventario)
# ------------------------------------------------------------
def crear_producto(nombre: str, precio: float, stock: int) -> bool:
    """
    Inserta un nuevo producto en la BD.
    Retorna True si se insertó, False si el nombre ya existe (viola UNIQUE).
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        # El CHECK precio >= 1 y stock >= 0 se aplican automáticamente en la BD.
        cur.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s);",
            (nombre, precio, stock)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.IntegrityError as e:
        # Si el nombre ya existe, la BD lanza este error.
        print(f"⚠️  Error de integridad: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al crear producto: {e}")
        return False

def buscar_por_texto(texto: str) -> List[Tuple[int, str, float, int]]:
    """
    Busca productos cuyo nombre contenga 'texto' (insensible a mayúsculas).
    Retorna una lista de tuplas: (id, nombre, precio, stock).
    """
    conn = get_connection()
    cur = conn.cursor()
    # ILIKE es la versión de LIKE que no distingue mayúsculas.
    cur.execute(
        "SELECT id, nombre, precio, stock FROM productos WHERE nombre ILIKE %s;",
        (f"%{texto}%",)
    )
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

def eliminar_por_nombre(nombre: str) -> bool:
    """
    Elimina un producto por su nombre exacto (insensible a mayúsculas).
    Retorna True si eliminó al menos una fila, False si no.
    """
    conn = get_connection()
    cur = conn.cursor()
    # Usamos ILIKE para insensibilidad, y LIMIT 1 por seguridad (aunque nombre es UNIQUE).
    cur.execute(
        "DELETE FROM productos WHERE nombre ILIKE %s;",
        (nombre,)
    )
    filas_afectadas = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return filas_afectadas > 0

def actualizar_precio(nombre: str, nuevo_precio: float) -> bool:
    """
    Actualiza el precio de un producto por su nombre exacto.
    Retorna True si actualizó, False si no encontró el producto.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE productos SET precio = %s WHERE nombre ILIKE %s;",
        (nuevo_precio, nombre)
    )
    filas_afectadas = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return filas_afectadas > 0

def obtener_todos() -> List[Tuple[int, str, float, int]]:
    """Devuelve todos los productos ordenados por nombre."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, precio, stock FROM productos ORDER BY nombre;")
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

def vaciar_tabla():
    """Elimina todos los productos de la tabla (para pruebas)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM productos;")
    conn.commit()
    cur.close()
    conn.close()