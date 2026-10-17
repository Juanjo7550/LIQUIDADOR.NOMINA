"""
Plantilla de configuración de la conexión a la base de datos.

INSTRUCCIONES DE USO:
1. Copie este archivo y renombre la copia como secret_config.py
   (en la misma carpeta raíz del proyecto).
2. Reemplace los valores de ejemplo por los datos reales de su
   base de datos PostgreSQL (por ejemplo, los que entrega Render).
3. NO suba secret_config.py al repositorio: ya está incluido en .gitignore.
"""

PGDATABASE = "nombre_de_la_base_de_datos"
PGUSER = "usuario"
PGPASSWORD = "contraseña"
PGHOST = "servidor.ejemplo.com"
PGPORT = 5432
