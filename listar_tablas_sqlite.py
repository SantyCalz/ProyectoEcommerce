import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

tablas_a_borrar = [
    'auth_user',
    'auth_user_groups',
    'auth_user_user_permissions',
    'productos_perfil'
]

for tabla in tablas_a_borrar:
    try:
        c.execute(f"DROP TABLE IF EXISTS {tabla};")
        print(f"Tabla '{tabla}' eliminada.")
    except Exception as e:
        print(f"Error eliminando {tabla}: {e}")

conn.commit()
conn.close()
