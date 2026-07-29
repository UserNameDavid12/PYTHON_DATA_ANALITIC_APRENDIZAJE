import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="inventario_db",
        user="postgres",
        password="1234"   # <--- CAMBIA por la contraseña que pusiste
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("✅ Conexión exitosa. Versión de PostgreSQL:", version[0])
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Error al conectar:", e)