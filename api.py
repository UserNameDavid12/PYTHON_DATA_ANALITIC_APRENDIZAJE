# ============================================================
# api.py - API REST para el sistema de inventario
# Desarrollado con FastAPI, expone los datos de PostgreSQL
# ============================================================

# Importamos las herramientas necesarias
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
import db

# ------------------------------------------------------------
# 1. CREAMOS LA APLICACIÓN FASTAPI
# ------------------------------------------------------------
app = FastAPI(
    title="API de Inventario",
    description="Sistema de gestión de productos con persistencia en PostgreSQL",
    version="1.0.0"
)

# ------------------------------------------------------------
# 2. MODELOS DE DATOS (Pydantic)
# ------------------------------------------------------------
class ProductoBase(BaseModel):
    """Modelo base para crear/actualizar un producto."""
    nombre: str
    precio: float
    stock: int

class ProductoResponse(ProductoBase):
    """Modelo que incluye el ID devuelto por la base de datos."""
    id: int

# ------------------------------------------------------------
# 3. ENDPOINTS (RUTAS) DE LA API
# ------------------------------------------------------------

# 3.1 - GET /productos → Devuelve todos los productos
@app.get("/productos", response_model=List[ProductoResponse])
def obtener_productos():
    """Obtiene la lista completa de productos del inventario."""
    try:
        resultados = db.obtener_todos()
        productos = [
            {"id": id_, "nombre": nom, "precio": float(precio), "stock": stock}
            for id_, nom, precio, stock in resultados
        ]
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}"
        )

# 3.2 - GET /productos/{id} → Devuelve un producto por su ID
@app.get("/productos/{id}", response_model=ProductoResponse)
def obtener_producto_por_id(id: int):
    """Obtiene un producto específico por su ID."""
    try:
        todos = db.obtener_todos()
        for id_, nom, precio, stock in todos:
            if id_ == id:
                return {"id": id_, "nombre": nom, "precio": float(precio), "stock": stock}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {id} no encontrado"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar producto: {str(e)}"
        )

# 3.3 - GET /buscar?q=texto → Busca productos por nombre
@app.get("/buscar", response_model=List[ProductoResponse])
def buscar_productos(q: str):
    """Busca productos cuyo nombre contenga la cadena 'q' (insensible a mayúsculas)."""
    try:
        resultados = db.buscar_por_texto(q)
        productos = [
            {"id": id_, "nombre": nom, "precio": float(precio), "stock": stock}
            for id_, nom, precio, stock in resultados
        ]
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en búsqueda: {str(e)}"
        )

# 3.4 - POST /productos → Crea un nuevo producto
@app.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoBase):
    """Crea un nuevo producto en el inventario."""
    try:
        if not producto.nombre or not producto.nombre.strip():
            raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")
        if producto.precio < 1:
            raise HTTPException(status_code=400, detail="El precio mínimo es $1")
        if producto.stock < 0:
            raise HTTPException(status_code=400, detail="El stock no puede ser negativo")

        exito = db.crear_producto(
            nombre=producto.nombre.strip(),
            precio=round(producto.precio, 2),
            stock=int(producto.stock)
        )
        if not exito:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El producto '{producto.nombre}' ya existe"
            )
        
        resultados = db.buscar_por_texto(producto.nombre)
        for id_, nom, precio, stock in resultados:
            if nom.lower() == producto.nombre.lower():
                return {"id": id_, "nombre": nom, "precio": float(precio), "stock": stock}
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Producto creado pero no se pudo recuperar"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}"
        )

# 3.5 - DELETE /productos/{nombre} → Elimina un producto por su nombre exacto
@app.delete("/productos/{nombre}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto_por_nombre(nombre: str):
    """Elimina un producto por su nombre exacto (insensible a mayúsculas)."""
    try:
        exito = db.eliminar_por_nombre(nombre)
        if not exito:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto '{nombre}' no encontrado"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar producto: {str(e)}"
        )

# 3.6 - PATCH /productos/{nombre}/descuento → Aplica descuento
@app.patch("/productos/{nombre}/descuento")
def aplicar_descuento(nombre: str, porcentaje: float):
    """Aplica un descuento porcentual a un producto existente."""
    try:
        if porcentaje < 0 or porcentaje > 100:
            raise HTTPException(
                status_code=400,
                detail="El porcentaje debe estar entre 0 y 100"
            )
        resultados = db.buscar_por_texto(nombre)
        producto = None
        for id_, nom, precio, stock in resultados:
            if nom.lower() == nombre.lower():
                producto = (id_, nom, precio, stock)
                break
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto '{nombre}' no encontrado"
            )
        id_, nom, precio_actual, stock = producto
        precio_actual_float = float(precio_actual)
        nuevo_precio = precio_actual_float * (1 - (porcentaje / 100.0))
        exito = db.actualizar_precio(nombre, nuevo_precio)
        if not exito:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar el precio"
            )
        return {
            "mensaje": f"Descuento del {porcentaje}% aplicado a '{nom}'",
            "precio_anterior": precio_actual_float,
            "precio_nuevo": nuevo_precio
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al aplicar descuento: {str(e)}"
        )

# 3.7 - NUEVO ENDPOINT: GET /productos/stock-bajo
@app.get("/productos/stock-bajo", response_model=List[ProductoResponse])
def obtener_productos_stock_bajo(limite: int = 5):
    """
    Devuelve todos los productos cuyo stock es menor al límite indicado.
    Por defecto, el límite es 5. Ejemplo: /productos/stock-bajo?limite=3
    """
    try:
        resultados = db.obtener_stock_bajo(limite)
        productos = [
            {"id": id_, "nombre": nom, "precio": float(precio), "stock": stock}
            for id_, nom, precio, stock in resultados
        ]
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos con stock bajo: {str(e)}"
        )

# 3.8 - GET / → Endpoint de bienvenida
@app.get("/")
def raiz():
    return {
        "mensaje": "Bienvenido a la API de Inventario",
        "documentacion": "/docs",
        "endpoints": [
            "GET /productos",
            "GET /productos/{id}",
            "GET /productos/stock-bajo?limite=5",
            "GET /buscar?q=texto",
            "POST /productos (con JSON)",
            "DELETE /productos/{nombre}",
            "PATCH /productos/{nombre}/descuento?porcentaje=10"
        ]
    }

# ------------------------------------------------------------
# 4. EJECUCIÓN (para desarrollo)
# ------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)