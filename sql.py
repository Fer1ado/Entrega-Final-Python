import sqlite3
from ulid import ULID

# abrimos la conexion con la base de datos
conexion = sqlite3.connect("productos_db.db")

# creamos el <cursor> para interactuar con la base de datos
cursor = conexion.cursor()

# cons esto creaos la tabla en la base de datos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
    id VARCHAR(40) PRIMARY KEY,
    nombre TEXT NOT NULL,
    stock INTEGER NOT NULL)
""")




print(id)


productos = [
        ["Cuchillo Chef", 30],
        ["Tabla de Cortar", 100],
        ["Olla a Presión", 20],
        ["Batidora de Mano", 15],
        ["Tenedor de Cocina", 200],
        ["Colador de Acero Inoxidable", 60],
        ["Espátula de Silicona", 75],
        ["Cazo de Hierro Fundido", 10],
        ["Cafetera Italiana", 40],
        ["Sartén Wok", 25],
        ["Rallador Multifunión", 50],
        ["Recipiente para Alimentos", 120],
        ["Tetera de Acero", 35],
        ["Exprimidor Manual", 80],
        ["Molinillo de Sal", 40],
        ["Rodillo de Madera", 30],
        ["Cucharón de Cocina", 90],
        ["Cucharas Medidoras", 11]
]

for producto in productos: 
    id = str(ULID())
    cursor.execute(f"INSERT INTO productos (id, nombre, stock) VALUES (?, ?,?)", (id, producto[0], producto[1]))


# con esto guardamos los cambios hechos
conexion.commit()
# cerramos la conexion del cursor
cursor.close()





#cerramos conexion con la base de datos
conexion.close()