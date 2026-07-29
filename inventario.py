# ============================================================
# ARCHIVO: inventario.py
# DESCRIPCIÓN: Sistema de gestión de inventario con persistencia en PostgreSQL.
#              La clase Inventario ahora usa la base de datos a través de db.py.
# ============================================================

# Importamos la capa de acceso a datos (la que creamos en db.py)
import db

# ------------------------------------------------------------
# 1. CLASE PRODUCTO (se mantiene igual, pero ya no se usa para almacenar)
#    La dejamos para representar objetos en memoria cuando sea necesario,
#    pero los datos reales viven en PostgreSQL.
# ------------------------------------------------------------
class Producto:
    """
    Representa un producto físico o digital con nombre, precio y stock.
    Se usa para crear objetos temporales, pero la persistencia está en la BD.
    """
    def __init__(self, nombre: str, precio: float, stock: int):
        # Validaciones básicas (igual que antes)
        if not nombre or not nombre.strip():
            raise ValueError("ERROR: El nombre del producto NO puede estar vacío.")
        if precio < 1:
            raise ValueError("ERROR: El precio mínimo es $1.")
        if stock < 0:
            raise ValueError("ERROR: El stock NO puede ser negativo.")
        
        self.nombre = nombre.strip()
        self.precio = round(precio, 2)
        self.stock = int(stock)

    def __str__(self) -> str:
        return f"🛒 {self.nombre} - ${self.precio:.2f} (Stock: {self.stock})"


# ------------------------------------------------------------
# 2. CLASE INVENTARIO (AHORA CON PERSISTENCIA EN POSTGRESQL)
# ------------------------------------------------------------
class Inventario:
    """
    Esta clase maneja el inventario, pero TODAS las operaciones
    se reflejan directamente en la base de datos PostgreSQL.
    """

    def __init__(self):
        """
        No necesitamos una lista en memoria. La base de datos es la fuente de verdad.
        """
        # self.__productos = []  # ¡ELIMINADO! Ya no se usa.
        pass  # No hace falta inicializar nada.

    # --------------------------------------------------------
    # MÉTODO 1: agregar
    # --------------------------------------------------------
    def agregar(self, producto: Producto) -> bool:
        """
        Agrega un producto a la base de datos.
        Retorna True si se insertó, False si ya existía (UNIQUE constraint).
        """
        # Llamamos a la función de db.py que ya maneja la inserción.
        # db.crear_producto devuelve True si se insertó, False si falló (duplicado).
        exito = db.crear_producto(producto.nombre, producto.precio, producto.stock)
        if exito:
            print(f"✅ Producto '{producto.nombre}' agregado exitosamente (BD).")
        else:
            print(f"⚠️  Advertencia: El producto '{producto.nombre}' YA EXISTE en la base de datos.")
        return exito

    # --------------------------------------------------------
    # MÉTODO 2: buscar_por_nombre
    # --------------------------------------------------------
    def buscar_por_nombre(self, texto: str) -> list:
        """
        Busca productos cuyo nombre CONTENGA el texto (insensible a mayúsculas).
        Retorna una lista de objetos Producto (creados a partir de los datos de la BD).
        """
        # Obtenemos los resultados de la base de datos como lista de tuplas.
        # db.buscar_por_texto devuelve [(id, nombre, precio, stock), ...]
        tuplas = db.buscar_por_texto(texto)
        
        # Convertimos cada tupla en un objeto Producto (para que el resto del código
        # no se entere de que estamos usando una base de datos).
        productos = []
        for id_, nombre, precio, stock in tuplas:
            # Creamos un objeto Producto temporal (solo para devolverlo).
            # No se guarda en la BD, solo es una representación en memoria.
            prod = Producto(nombre, precio, stock)
            # Opcional: podemos guardar el ID en un atributo extra si lo necesitamos.
            # prod.id = id_  (lo dejamos comentado por ahora)
            productos.append(prod)
        return productos

    # --------------------------------------------------------
    # MÉTODO 3: eliminar_por_nombre
    # --------------------------------------------------------
    def eliminar_por_nombre(self, nombre: str) -> bool:
        """
        Elimina un producto de la base de datos por su nombre exacto.
        Retorna True si se eliminó, False si no se encontró.
        """
        # db.eliminar_por_nombre devuelve True si eliminó al menos una fila.
        exito = db.eliminar_por_nombre(nombre)
        if exito:
            print(f"🗑️  Producto '{nombre}' eliminado exitosamente (BD).")
        else:
            print(f"❌ No se encontró el producto '{nombre}' para eliminar.")
        return exito

    # --------------------------------------------------------
    # MÉTODO 4: aplicar_descuento (CORREGIDO)
    # --------------------------------------------------------
    def aplicar_descuento(self, nombre: str, porcentaje: float) -> bool:
        """
        Busca un producto por su nombre exacto, calcula el nuevo precio
        aplicando el descuento, y actualiza la base de datos.
        Retorna True si se actualizó, False si no se encontró.
        """
        # PASO 1: Obtener el producto actual de la BD
        resultados = db.buscar_por_texto(nombre)
        producto_encontrado = None
        for id_, nom, precio, stock in resultados:
            if nom.lower() == nombre.lower():  # Comparación exacta (insensible)
                producto_encontrado = (id_, nom, precio, stock)
                break
        
        if not producto_encontrado:
            print(f"❌ No se encontró el producto '{nombre}' para aplicar descuento.")
            return False
        
        # PASO 2: Calcular el nuevo precio.
        id_, nom, precio_actual, stock = producto_encontrado
        
        # 🔧 SOLUCIÓN: Convertimos 'Decimal' a 'float' para poder operar.
        # PostgreSQL devuelve Decimal para la columna DECIMAL.
        # Python no permite multiplicar Decimal * Float directamente.
        precio_actual_float = float(precio_actual)
        nuevo_precio = precio_actual_float * (1 - (porcentaje / 100.0))
        
        # PASO 3: Actualizar en la base de datos usando la función de db.py.
        # db.actualizar_precio devuelve True si actualizó.
        exito = db.actualizar_precio(nombre, nuevo_precio)
        if exito:
            print(f"💰 Descuento del {porcentaje}% aplicado a '{nom}'. Nuevo precio: ${nuevo_precio:.2f}")
        else:
            print(f"❌ Error al actualizar el precio de '{nombre}'.")
        return exito

    # --------------------------------------------------------
    # MÉTODO 5: mostrar_inventario (MEJORADO: obtiene datos de la BD)
    # --------------------------------------------------------
    def mostrar_inventario(self):
        """
        Muestra todos los productos obtenidos de la base de datos.
        Si está vacío, lo indica.
        """
        # Obtenemos todos los productos de la BD.
        tuplas = db.obtener_todos()
        
        if not tuplas:
            print("📭 El inventario está VACÍO. Aún no hay productos.")
            return
        
        cantidad = len(tuplas)
        print("\n" + "="*50)
        if cantidad == 1:
            print("📦 1 PRODUCTO EN STOCK:")
        else:
            print(f"📦 INVENTARIO ACTUAL ({cantidad} productos):")
        print("="*50)
        
        for id_, nombre, precio, stock in tuplas:
            # Mostramos directamente los datos (no necesitamos crear objetos Producto).
            print(f"  • 🛒 {nombre} - ${precio:.2f} (Stock: {stock}) [ID: {id_}]")
        print("="*50 + "\n")


# ============================================================
# BLOQUE DE PRUEBAS (se ejecuta con 'python inventario.py')
# ============================================================
if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE INVENTARIO (CON POSTGRESQL)...\n")

    # Limpiamos la tabla para empezar desde cero (evita datos residuales).
    # ¡Cuidado! Esto borra todos los productos de la BD.
    db.vaciar_tabla()
    print("🗑️  Base de datos vaciada para comenzar pruebas limpias.\n")

    # Crear instancia del Inventario
    mi_inventario = Inventario()

    # 1. Crear algunos productos (objetos en memoria)
    try:
        p1 = Producto("Laptop Gamer", 1200.50, 5)
        p2 = Producto("Mouse Inalámbrico", 25.99, 50)
        p3 = Producto("Monitor Led", 350.00, 3)
    except ValueError as e:
        print(f"🔥 Error al crear producto: {e}")

    # 2. Agregarlos a la base de datos
    print("--- Agregando productos ---")
    mi_inventario.agregar(p1)
    mi_inventario.agregar(p2)
    mi_inventario.agregar(p3)

    # 3. Mostrar el inventario (ahora desde PostgreSQL)
    mi_inventario.mostrar_inventario()

    # 4. Buscar productos
    print("--- Buscando productos con 'mouse' ---")
    resultados_mouse = mi_inventario.buscar_por_nombre("mouse")
    if resultados_mouse:
        for prod in resultados_mouse:
            print(f"  Encontrado: {prod}")
    else:
        print("  No se encontraron productos.")
    print()

    print("--- Buscando productos con 'lap' ---")
    resultados_lap = mi_inventario.buscar_por_nombre("lap")
    for prod in resultados_lap:
        print(f"  Encontrado: {prod}")
    print()

    # 5. Aplicar descuento
    print("--- Aplicando descuentos ---")
    mi_inventario.aplicar_descuento("Laptop Gamer", 10)
    mi_inventario.aplicar_descuento("Tablet", 15)  # No existe

    # 6. Mostrar inventario después del descuento
    mi_inventario.mostrar_inventario()

    # 7. Probar eliminación
    print("--- Probando eliminar ---")
    mi_inventario.eliminar_por_nombre("Mouse Inalámbrico")
    mi_inventario.mostrar_inventario()

    # 8. Insertar un producto con precio mínimo ($1) para probar la validación
    print("--- Insertando producto con precio $1 ---")
    p4 = Producto("Producto Mínimo", 1.00, 2)
    mi_inventario.agregar(p4)
    mi_inventario.mostrar_inventario()

    print("🏁 Pruebas finalizadas. Revise los mensajes arriba.")
    print("👉 Ahora abre DBeaver y ejecuta: SELECT * FROM productos;")
    print("   Verás que los datos persisten incluso después de cerrar Python.")