# ============================================================
# ARCHIVO: inventario.py
# DESCRIPCIÓN: Sistema de gestión de inventario con POO pura.
#              Aprenderás: Encapsulamiento, Validaciones,
#              Recorridos de listas, Filtros y Setters.
# ============================================================

# ------------------------------------------------------------
# 1. CLASE PRODUCTO (La base de todo nuestro sistema)
# ------------------------------------------------------------
class Producto:
    """
    Representa un producto físico o digital con nombre, precio y stock.
    Usa 'properties' (getters/setters) para validar los datos en TODO momento.
    """

    def __init__(self, nombre: str, precio: float, stock: int):
        """
        Constructor: Se ejecuta cuando haces 'Producto("Laptop", 1200, 5)'.
        NOTA: No asignamos directamente a self.nombre, self.precio, self.stock.
        Llamamos a los SETTERS (los métodos con @...setter) para que validen.
        """
        # IMPORTANTE: Aquí usamos 'self.nombre = ...' (no self._nombre)
        # porque Python busca el método 'setter' automáticamente.
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    # --------------------------------------------------------
    # GETTER Y SETTER para 'nombre'
    # --------------------------------------------------------
    @property
    def nombre(self) -> str:
        """GETTER: Cuando escribes 'mi_producto.nombre', devuelve esto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        """
        SETTER: Cuando escribes 'mi_producto.nombre = "Nuevo"', se ejecuta esto.
        Aquí metemos las REGLAS DE NEGOCIO (validaciones).
        """ 
        # Validación 1: ¿El texto está vacío o solo tiene espacios?
        if not valor or not valor.strip():
            # 'raise ValueError' detiene el programa y lanza un error claro.
            raise ValueError("ERROR: El nombre del producto NO puede estar vacío.")
        
        # Si pasa la validación, guardamos el valor limpio (sin espacios al inicio/final)
        # y lo asignamos a la variable PRIVADA '_nombre' (el guion bajo indica "privado").
        self._nombre = valor.strip()

    # --------------------------------------------------------
    # GETTER Y SETTER para 'precio'  (MEJORADO: Precio mínimo $1)
    # --------------------------------------------------------
    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float):
        # --- NUEVA VALIDACIÓN ---
        # Ahora el precio NO puede ser 0 ni negativo. El mínimo es $1.
        # Esto protege tu negocio: ningún producto puede venderse a $0.
        if valor < 1:
            raise ValueError("ERROR: El precio mínimo es $1. No se permiten precios menores a 1.")
        
        # Redondeamos a 2 decimales para evitar problemas con centavos (ej: 1.9999 -> 2.00)
        self._precio = round(valor, 2)

    # --------------------------------------------------------
    # GETTER Y SETTER para 'stock'
    # --------------------------------------------------------
    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int):
        # Validación: El stock no puede ser negativo.
        if valor < 0:
            raise ValueError("ERROR: El stock NO puede ser negativo.")
        
        # Aseguramos que sea entero (por si alguien pasa 5.0, lo convertimos a 5).
        self._stock = int(valor)

    # --------------------------------------------------------
    # MÉTODO MÁGICO: __str__ (Para mostrar el producto bonito)
    # --------------------------------------------------------
    def __str__(self) -> str:
        """
        Cuando usas 'print(mi_producto)', Python busca este método.
        Es la forma elegante de mostrar el estado del objeto.
        """
        return f"🛒 {self.nombre} - ${self.precio:.2f} (Stock: {self.stock})"


# ------------------------------------------------------------
# 2. CLASE INVENTARIO (El contenedor/gestor de productos)
# ------------------------------------------------------------
class Inventario:
    """
    Esta clase maneja una lista de productos.
    Proporciona métodos para agregar, buscar, modificar y mostrar.
    """

    def __init__(self):
        """
        Inicializa el inventario con una lista VACÍA y PRIVADA.
        El doble guion bajo '__' se llama "Name Mangling".
        Hace que sea más difícil acceder desde fuera (protección).
        """
        self.__productos = []  # Lista privada donde se guardarán los objetos Producto

    # --------------------------------------------------------
    # MÉTODO 1: agregar
    # --------------------------------------------------------
    def agregar(self, producto: Producto) -> bool:
        """
        Agrega un producto a la lista, pero SOLO si no existe otro con el mismo nombre.
        Retorna True si se agregó, False si ya existía.

        ¿Por qué retornar un bool? Para que el programa sepa si tuvo éxito o no.
        """
        # PASO 1: Recorremos la lista actual para buscar duplicados.
        # Aquí aplicamos el concepto de "recorrido de colecciones".
        # ¿Qué tipo de dato es self.__productos? Es una LISTA.
        # ¿Cómo la recorro? Con un bucle 'for'.
        for prod in self.__productos:
            # Comparamos el nombre IGNORANDO mayúsculas/minúsculas.
            # Esto evita que tengas "Laptop" y "laptop" como dos productos distintos.
            if prod.nombre.lower() == producto.nombre.lower():
                # Si encontramos uno igual, mostramos un aviso y retornamos False (no se agregó).
                print(f"⚠️  Advertencia: El producto '{producto.nombre}' YA EXISTE en el inventario.")
                return False

        # PASO 2: Si terminó el bucle y NO encontró duplicado, lo agregamos.
        self.__productos.append(producto)
        print(f"✅ Producto '{producto.nombre}' agregado exitosamente.")
        return True

    # --------------------------------------------------------
    # MÉTODO 2: buscar_por_nombre
    # --------------------------------------------------------
    def buscar_por_nombre(self, texto: str) -> list:
        """
        Busca productos cuyo nombre CONTENGA el texto indicado (sin importar mayúsculas).
        Retorna UNA NUEVA LISTA con los resultados. Si no encuentra nada, retorna lista vacía.

        AQUÍ APRENDES LA TÉCNICA DE FILTRADO.
        Esto es EXACTAMENTE lo que haces cuando filtras datos en Excel, Pandas o SQL.
        """
        # PASO 1: Limpiamos el texto de búsqueda (quitamos espacios y lo ponemos en minúscula).
        texto_busqueda = texto.lower().strip()
        
        # PASO 2: Filtramos usando "List Comprehension" (Comprensión de listas).
        # Esta es una de las herramientas MÁS PODEROSAS de Python.
        # Traducción al español:
        #   "Crea una nueva lista con 'prod' para cada 'prod' en mi lista de productos,
        #    pero solo si 'texto_busqueda' está dentro de 'prod.nombre' en minúsculas."
        resultados = [
            prod for prod in self.__productos 
            if texto_busqueda in prod.nombre.lower()
        ]
        
        # PASO 3: Retornamos la nueva lista.
        # NOTA: No modificamos la lista original, creamos una copia filtrada.
        return resultados

    # --------------------------------------------------------
    # MÉTODO 3: aplicar_descuento
    # --------------------------------------------------------
    def aplicar_descuento(self, nombre: str, porcentaje: float) -> bool:
        """
        Busca un producto por su nombre EXACTO (ignorando mayúsculas).
        Si lo encuentra, le reduce el precio según el porcentaje indicado.
        Retorna True si aplicó el descuento, False si no encontró el producto.

        ¿Por qué es importante el SETTER aquí?
        Cuando hagamos 'producto.precio = nuevo_precio', se dispara el setter de Producto,
        y automáticamente validará que el nuevo precio no sea negativo.
        """
        # PASO 1: Recorremos la lista con un bucle 'for'.
        for prod in self.__productos:
            # Comparamos el nombre exacto (ignorando mayúsculas).
            if prod.nombre.lower() == nombre.lower():
                
                # PASO 2: Calculamos el nuevo precio.
                # Ejemplo: si precio=100 y porcentaje=10, nuevo = 100 * (1 - 0.10) = 90.
                nuevo_precio = prod.precio * (1 - (porcentaje / 100.0))
                
                # PASO 3: Asignamos el nuevo precio USANDO EL SETTER.
                # Python automáticamente llamará a 'precio.setter' y validará que no sea negativo.
                # Si alguien pone porcentaje=200 (descuento del 200%), el setter lanzará error.
                prod.precio = nuevo_precio
                
                print(f"💰 Descuento del {porcentaje}% aplicado a '{prod.nombre}'. Nuevo precio: ${prod.precio:.2f}")
                return True
        
        # Si terminó el bucle y no encontró el nombre, mostramos aviso.
        print(f"❌ No se encontró el producto '{nombre}' para aplicar descuento.")
        return False

    # --------------------------------------------------------
    # MÉTODO NUEVO: eliminar_por_nombre  (TAREA 2)
    # --------------------------------------------------------
    def eliminar_por_nombre(self, nombre: str) -> bool:
        """
        Busca un producto por su nombre EXACTO (ignorando mayúsculas).
        Si lo encuentra, lo elimina de la lista usando pop().
        Retorna True si se eliminó, False si no se encontró.

        ¿Por qué usamos 'enumerate'?
        Porque necesitamos el ÍNDICE (posición) del producto para eliminarlo con pop().
        """
        # PASO 1: Recorremos la lista con 'enumerate' para obtener índice (i) y objeto (prod).
        for i, prod in enumerate(self.__productos):
            # Comparamos el nombre exacto (ignorando mayúsculas).
            if prod.nombre.lower() == nombre.lower():
                
                # PASO 2: Eliminamos el producto usando 'pop(i)'.
                # 'pop' borra el elemento en la posición 'i' y lo devuelve.
                # Guardamos el nombre para mostrarlo en el mensaje.
                producto_eliminado = self.__productos.pop(i)
                print(f"🗑️  Producto '{producto_eliminado.nombre}' eliminado exitosamente.")
                return True
        
        # Si terminó el bucle y no encontró el nombre, mostramos aviso.
        print(f"❌ No se encontró el producto '{nombre}' para eliminar.")
        return False

    # --------------------------------------------------------
    # MÉTODO 4: mostrar_inventario  (MEJORADO: Singular/Plural - TAREA 3)
    # --------------------------------------------------------
    def mostrar_inventario(self):
        """
        Imprime en pantalla todos los productos del inventario.
        Si está vacío, lo indica.
        Si tiene 1 producto, muestra un mensaje especial en SINGULAR.
        Si tiene más de 1, muestra el número total en PLURAL.
        """
        # PASO 1: Verificar si la lista está vacía.
        # En Python, 'if not lista' es True si la lista está vacía.
        if not self.__productos:
            print("📭 El inventario está VACÍO. Aún no hay productos.")
            return
        
        # PASO 2: Contamos cuántos productos hay usando len().
        cantidad = len(self.__productos)
        
        # PASO 3: Mostramos el encabezado adaptado a la cantidad.
        print("\n" + "="*50)
        if cantidad == 1:
            # Si solo hay 1, usamos mensaje en SINGULAR (es más profesional).
            print("📦 1 PRODUCTO EN STOCK:")
        else:
            # Si hay más de 1, mostramos el número total.
            print(f"📦 INVENTARIO ACTUAL ({cantidad} productos):")
        print("="*50)
        
        # PASO 4: Recorremos e imprimimos cada producto usando __str__.
        for prod in self.__productos:
            print(f"  • {prod}")
        print("="*50 + "\n")


# ============================================================
# BLOQUE DE PRUEBAS (Solo se ejecuta si corres este archivo directamente)
# ============================================================
if __name__ == "__main__":
    """
    Este bloque se ejecuta SOLO cuando haces 'python inventario.py' en la terminal.
    Si otro archivo importa este código (import inventario), esto NO se ejecuta.
    Es el lugar perfecto para hacer pruebas sin afectar el resto del sistema.
    """

    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE INVENTARIO...\n")

    # 1. Crear una instancia del Inventario (nuestro "cajón" de productos)
    mi_inventario = Inventario()

    # 2. Crear algunos productos (se validan automáticamente al crearse)
    try:
        # Producto válido
        p1 = Producto("Laptop Gamer", 1200.50, 5)
        
        # Producto válido
        p2 = Producto("Mouse Inalámbrico", 25.99, 50)
        
        # Producto válido (MONITOR, para tener 3 productos inicialmente)
        p3 = Producto("Monitor Led", 350.00, 3)  # <--- Cambié el precio a 350 para que sea realista
        
        # Intento de producto inválido (PREMIUM: Esto lanzará ERROR y detendrá la prueba)
        # p_invalido = Producto("", -10, -5)  # Descomenta esta línea para ver cómo "explota" bonito.
        
    except ValueError as e:
        # Si el producto inválido lanza error, lo atrapamos y mostramos el mensaje.
        print(f"🔥 Error controlado al crear producto: {e}\n")

    # 3. Agregar productos al inventario (el método evita duplicados)
    print("--- Agregando productos ---")
    mi_inventario.agregar(p1)  # Debería agregarse
    mi_inventario.agregar(p2)  # Debería agregarse
    mi_inventario.agregar(p3)  # Debería agregarse (Monitor no duplica a Laptop)

    # 4. Mostrar el inventario completo (Verás "INVENTARIO ACTUAL (3 productos):")
    mi_inventario.mostrar_inventario()

    # 5. Buscar productos que contengan "mouse" (insensible a mayúsculas)
    print("--- Buscando productos con 'mouse' ---")
    resultados_mouse = mi_inventario.buscar_por_nombre("mouse")
    if resultados_mouse:
        for prod in resultados_mouse:
            print(f"  Encontrado: {prod}")
    else:
        print("  No se encontraron productos.")
    print()

    # 6. Buscar productos que contengan "lap" (debería encontrar la laptop)
    print("--- Buscando productos con 'lap' ---")
    resultados_lap = mi_inventario.buscar_por_nombre("lap")
    for prod in resultados_lap:
        print(f"  Encontrado: {prod}")
    print()

    # 7. Aplicar descuento del 10% a la "Laptop Gamer" (debe activar el setter)
    print("--- Aplicando descuentos ---")
    mi_inventario.aplicar_descuento("Laptop Gamer", 10)  # Baja de 1200.50 a 1080.45

    # 8. Intentar aplicar descuento a un producto que no existe
    mi_inventario.aplicar_descuento("Tablet", 15)  # Debe decir que no existe

    # 9. Intentar aplicar descuento del 200% (Esto activará la validación del setter)
    #    ¿Qué crees que pasará? El setter de precio lanzará un error porque quedaría negativo.
    #    Descomenta la siguiente línea para probar cómo el sistema protege tu negocio.
    # mi_inventario.aplicar_descuento("Mouse Inalámbrico", 200)  

    # 10. Mostrar el inventario después de los descuentos (siguen 3 productos)
    mi_inventario.mostrar_inventario()

    # ================================================================
    # NUEVAS PRUEBAS PARA LAS TAREAS 1, 2 y 3 (Validación $1, Eliminar, Singular)
    # ================================================================
    print("\n" + "="*50)
    print("🧪 INICIANDO PRUEBAS DE LAS NUEVAS FUNCIONALIDADES")
    print("="*50)

    # --- PRUEBA 1: Validación de precio mínimo ($1) ---
    print("\n--- Probando validación de precio mínimo ($1) ---")
    try:
        # Intentamos crear un producto con precio $0 (DEBERÍA FALLAR)
        producto_con_precio_cero = Producto("Producto Prohibido", 0, 10)
        print("❌ ERROR: El sistema PERMITIÓ precio $0 (esto está mal).")
    except ValueError as e:
        print(f"🔥 Correcto: El sistema RECHAZÓ precio $0. Error: {e}")
    
    try:
        # Intentamos crear un producto con precio $0.50 (DEBERÍA FALLAR)
        producto_con_precio_bajo = Producto("Otro Prohibido", 0.50, 5)
        print("❌ ERROR: El sistema PERMITIÓ precio $0.50 (esto está mal).")
    except ValueError as e:
        print(f"🔥 Correcto: El sistema RECHAZÓ precio $0.50. Error: {e}")
    
    # Intentamos crear un producto con $1.00 (SÍ DEBE FUNCIONAR)
    try:
        producto_valido = Producto("Producto Mínimo", 1.00, 2)
        mi_inventario.agregar(producto_valido)
        print("✅ Correcto: Producto con precio $1.00 agregado exitosamente (validación pasó).")
    except ValueError as e:
        print(f"❌ ERROR: El sistema RECHAZÓ precio $1.00 (esto está mal). Error: {e}")

    # --- PRUEBA 2: Eliminar productos (método eliminar_por_nombre) ---
    print("\n--- Probando ELIMINAR productos ---")
    # Eliminar el Mouse (que existe)
    mi_inventario.eliminar_por_nombre("Mouse Inalámbrico")
    
    # Eliminar el Monitor (que existe)
    mi_inventario.eliminar_por_nombre("Monitor Led")
    
    # Intentar eliminar un producto que NO existe
    mi_inventario.eliminar_por_nombre("Audífonos")
    
    # --- PRUEBA 3: Mostrar inventario con 1 producto (debe usar SINGULAR) ---
    print("\n--- Mostrando inventario después de eliminar (SOLO QUEDA 1 PRODUCTO) ---")
    # Después de eliminar Mouse y Monitor, solo queda la "Laptop Gamer".
    # Aquí debe aparecer el mensaje "📦 1 PRODUCTO EN STOCK:" (en singular).
    mi_inventario.mostrar_inventario()

    # --- PRUEBA 4: Eliminar el último producto para dejar vacío ---
    print("\n--- Eliminando el último producto (Laptop Gamer) ---")
    mi_inventario.eliminar_por_nombre("Laptop Gamer")
    
    print("\n--- Mostrando inventario vacío ---")
    mi_inventario.mostrar_inventario()  # Debe decir "📭 El inventario está VACÍO."

    print("\n" + "="*50)
    print("🏁 TODAS LAS PRUEBAS FINALIZADAS. REVISE LOS MENSAJES ARRIBA.")
    print("="*50)