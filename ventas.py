# Paso 1: La Clase con Tipos y Validación (La Base Sólida)

# ¿Qué has aprendido aquí que sirve para CUALQUIER lenguaje?

# El principio de "Fail Fast" (Fallar Rápido): Si te llegan datos malos, 
# el sistema debe explotar en el momento de la creación (raise ValueError), 
# no 3 horas después cuando intentes vender un producto con stock negativo.
# En Java usas throw new IllegalArgumentException(), 
# en C# throw new ArgumentException(). Es el mismo concepto.

# class Producto:
#     def __init__(self, nombre: str, precio: float, stock: int):
#         # 1. VALIDACIÓN (La primera línea de defensa de tu sistema)
#         if not nombre or not nombre.strip():
#             raise ValueError("El nombre del producto es obligatorio.")
#         if precio < 0:
#             raise ValueError("El precio no puede ser negativo.")
#         if stock < 0:
#             raise ValueError("El stock no puede ser negativo.")
#         if not isinstance(stock, int):
#             raise TypeError("El stock debe ser un número entero.")

#         # 2. ASIGNACIÓN (Solo si pasó las validaciones)
#         self.nombre = nombre.strip()
#         self.precio = precio
#         self.stock = stock

#     def __str__(self) -> str:
#         return f"{self.nombre} - ${self.precio:.2f} (Stock: {self.stock})"

# --------------------------------------------------------------------------------------

# Paso 2: El Encapsulamiento (El Secreto de los Sistemas Robusto)
# Ahora mismo, aunque validaste en el __init__, 
# un programador malvado puede hacer esto:

# pan = Producto("Pan", 1.5, 10)
# pan.precio = -100  # ¡Tu validación del __init__ no sirve para esto!

# Para evitarlo, en todos los lenguajes se usa el encapsulamiento.
# En Python se hace con @property. Mira este salto de calidad:

# Traducción a otros lenguajes (para que veas que es universal):
# En Java/C#: esto se llama Getters y Setters (getNombre(), setNombre(valor)).
# En JavaScript (TypeScript): se llaman accessors (get nombre(), set nombre(valor)).
# # ¿Por qué es tan importante? Porque ahora, si alguien intenta hacer 
# pan.precio = -100, el sistema lanza un error en el momento, 
# protegiendo la integridad de tu negocio.

class Producto:
    def __init__(self, nombre: str, precio: float, stock: int):
        self.nombre = nombre  # Llama al setter de nombre
        self.precio = precio  # Llama al setter de precio
        self.stock = stock    # Llama al setter de stock

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = valor

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int):
        if valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = valor

    def __str__(self) -> str:
        return f"{self.nombre} - ${self.precio:.2f} (Stock: {self.stock})"