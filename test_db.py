# ============================================================
# test_db.py - Pruebas de la capa de acceso a datos (db.py)
# ============================================================
from db import crear_producto, obtener_todos, vaciar_tabla

def main():
    print("🧪 INICIANDO PRUEBAS DE CONEXIÓN A PostgreSQL...\n")

    # 1. Limpiar la tabla para empezar desde cero (evita duplicados)
    vaciar_tabla()
    print("🗑️  Tabla 'productos' vaciada correctamente.\n")

    # 2. Insertar productos de prueba
    print("--- Insertando productos ---")
    producto1 = crear_producto("Laptop Gamer", 1200.50, 5)
    if producto1:
        print("✅ 'Laptop Gamer' insertado.")
    else:
        print("⚠️  'Laptop Gamer' ya existía (o error).")

    producto2 = crear_producto("Mouse Inalámbrico", 25.99, 50)
    if producto2:
        print("✅ 'Mouse Inalámbrico' insertado.")
    else:
        print("⚠️  'Mouse Inalámbrico' ya existía (o error).")

    # 3. Insertar un producto duplicado (debe fallar, es una prueba controlada)
    print("\n--- Probando duplicado (debe fallar) ---")
    duplicado = crear_producto("Laptop Gamer", 999.99, 3)
    if not duplicado:
        print("✅ Correcto: El duplicado fue RECHAZADO por la base de datos (UNIQUE constraint).")
    else:
        print("❌ ERROR: El duplicado no debería haberse insertado.")

    # 4. Obtener y mostrar todos los productos
    print("\n📦 PRODUCTOS GUARDADOS EN POSTGRESQL:")
    productos = obtener_todos()
    if productos:
        for prod in productos:
            # prod es una tupla: (id, nombre, precio, stock)
            print(f"  ID: {prod[0]} | {prod[1]} | ${prod[2]:.2f} | Stock: {prod[3]}")
    else:
        print("  No hay productos en la base de datos.")

    print("\n🏁 Pruebas finalizadas.")
    print("👉 Ahora abre DBeaver, haz clic en la tabla 'productos' y ejecuta:")
    print("   SELECT * FROM productos;")
    print("   ¡Verás los datos persistidos en la base de datos!")

if __name__ == "__main__":
    main()