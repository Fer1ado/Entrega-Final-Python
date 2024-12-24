# IMPORTACIONES
from rich.console import Console
from rich.table import Table
from rich import print
from ulid import ULID
from colorama import *
import sqlite3



def print_status(status):
    print(f"[bold blue italic] {status} [/]")

def print_error(status):
    print(f"[bold red italic] {status} [/]" )

def print_info(status1, status2 = ""):
    print(f"[bold green italic] {status1} {status2} [/]")

def interaction(status):
    return input(Fore.RED + Back.MAGENTA + status)

init(autoreset=True)

def generate_table(name, data):
    table = Table(title=name)
    table.add_column("Entrada", justify="left")
    table.add_column("ID del producto", justify="center", style="cyan")
    table.add_column("Producto", justify="center", no_wrap=True)
    table.add_column("STOCK", justify="right", style="yellow")

    for item in data:
        table.add_row(str(data.index(item)), str(item[0]), str(item[1]), str(item[2]))
    
    console = Console()
    console.print(table)

# FUNCIONES
def mostrar_producto(producto: dict):
    print(f"nombre: {producto["nombre"]} - stock: {producto["stock"]}")


def cargar_nuevo_producto():
    print_status("cargando datos...")
    # datos de producto
    nombre_producto = interaction("Ingrese el nombre del producto: ")
    stock_producto = int( interaction("Ingrese el stock: ") )
    id = str(ULID())

    # conexión con la DB
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO productos (id, nombre, stock) values (?, ?, ?)                   
    """, (id, nombre_producto, stock_producto))

    # mensaje de confirmación
    print_info(f"Producto {nombre_producto} cargado con éxito")

    # commit de los cambios
    conexion.commit()
    cursor.close()
    mostrar_productos()


def mostrar_productos():
    print_status("mostrando datos...")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, stock FROM productos")
    productos_db = cursor.fetchall()
    
    # crea la tabla
    generate_table("LISTADO COMPLETO DE PRODUCTOS DEL BAZAR", productos_db)
    cursor.close()

def borrar_producto():
    # datos del usuario
    print_status("Borrando producto...")
    id_usuario = interaction("Ingrese el id para borrar: ")
    # interacicon con db
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM productos WHERE id=?", (id_usuario,))
    producto_encontrado = cursor.fetchall()

    if len(producto_encontrado) == 0:
        print_error("El producto no fue encontrado")
        return

    else: 
        cursor.execute("DELETE FROM productos WHERE id=?", (id_usuario,))
        # mensaje de devolucion
        print_info(f"Producto borrado con éxito {producto_encontrado}")
        conexion.commit()

    cursor.close()

def editar_producto():
    print_status("Editando Producto...")
    # datos del usuario
    id_usuario = interaction("Ingrese el id para modificar: ")
    # interacicon con db
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos where id=?", (id_usuario,))
    productos_encontrados = cursor.fetchall()
    print(productos_encontrados)

    if len(productos_encontrados) == 0:
        print_error("El producto no fue encontrado")
        return
    # datos del usuario 
    print_info("Se seleccionó el siguiente producto para modificar: ",productos_encontrados[0])
    stock = int( interaction("Ingrese el nuevo stock: ") )
    # interacicon con db
    cursor.execute("UPDATE productos SET stock=? where id=?", (stock, id_usuario))
    print_info(f"Producto modificado con éxito, nuevo Stock es: {stock} unidades")
    conexion.commit()
    cursor.close()


def reporte_bajo_stock():
    print_status("Reporte de bajo Stock...")
    # datos del usuario 
    cantidad_minima = int( interaction("Ingrese el numero desde el cual considera bajo stock: ") )
   
    # interacicon con db
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, stock FROM productos WHERE stock < ?", (cantidad_minima,))
    productos_db = cursor.fetchall()
    
    if len(productos_db) == 0:
        print_error("No hay ningun producto de bajo stock")
        return
    
    #Genero tabla con items
    generate_table("PRODUCTOS CON BAJO STOCK", productos_db) 
    cursor.close()
    
def buscar_por_nombre():
    print_status("Buscando  por Nombre...")
    # datos del usuario 
    nombre_a_buscar = interaction("Ingrese el nombre a buscar: ")
    
    # interacicon con db
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM productos WHERE nombre LIKE '%{(str(nombre_a_buscar))}%' ")
    productos_encontrados = cursor.fetchall()

    if len(productos_encontrados) < 1:
        print_error("El producto no fue encontrado")

    #Genero tabla con items
    else:
        generate_table("RESULTADO DE BUSQUEDA POR NOMBRE", productos_encontrados)

    cursor.close()

# INICIO DE APLICACION
# abrimos la conexion con la base de datos
conexion = sqlite3.connect("productos_db.db")

listado_productos = []
opcion = "in"

# MENU PRINCIPAL
while opcion != "0":
    # print opciones
    print("""


    [bold italic yellow on red blink]BIEVENIDO AL BAZAR DE CACHO[/]

    [bold magenta italic]QUE TENES GANAS DE HACER?:[/]
          
          1 - cargar datos
          2 - mostrar datos
          3 - buscar por nombre
          4 - editar producto
          5 - borrar producto
          6 - reporte bajo stock
          0 - salir
    """)
    opcion = input("Ingrese una opcion: ")
    if opcion == "1":
        cargar_nuevo_producto()
    elif opcion == "2":
        mostrar_productos()
    elif opcion == "3":
        buscar_por_nombre()
    elif opcion == "4":
        editar_producto()
    elif opcion == "5":
        borrar_producto()
    elif opcion == "6":
        reporte_bajo_stock()
    elif opcion == "0":
        print("Gracias por usar la app")
        conexion.close()
    else:
        print("Opcion incorrecta, intente de nuevo")