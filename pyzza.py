import sqlite3

# Conectar a la base de datos SQLite (se creará si no existe)
conn = sqlite3.connect('pyzza.db')
db = conn.cursor()

logo = """
  _____
 |  __ \\                   
 | |__) |   _ __________ _ 
 |  ___/ | | |_  /_  / _` |
 | |   | |_| |/ / / / (_| |
 |_|    \\__, /___/___\\__,_|
         __/ |             
        |___/         
"""

# Crear la tabla de productos si no existe
db.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    cantidad INT NOT NULL,
    moneda TEXT NOT NULL
)
''')
conn.commit()


def promedio(lista):
    suma = 0
    for prod in lista:
        suma += prod[1]
    return suma / len(lista)


def maximo(productos):
    # Inicializar el mayor como el menor valor posible
    precio_mayor = 0
    mayor = ["", 0]

    # Recorrer la lista y actualizar el valor del mayor si encontramos un valor mayor
    for elemento in productos:
        if elemento[1] > precio_mayor:
            mayor = elemento
            precio_mayor = elemento[1]

    return mayor


def minimo(productos):
    # Inicializar el mayor como el menor valor posible
    precio_menor = 9999999999999999999
    menor = ["", 0]

    # Recorrer la lista y actualizar el valor del mayor si encontramos un valor mayor
    for elemento in productos:
        if elemento[1] < precio_menor:
            menor = elemento
            precio_menor = elemento[1]

    return menor


def cargar_producto():
    nombre = input("Ingrese el nombre del producto: ")
    while nombre != "":
        precio = float(input("Ingrese el precio de " + nombre + ": "))
        cantidad = int(input("Ingrese la cantidad de " + nombre + ": "))
        moneda = input("Ingrese la criptomoneda con la que pagar " + nombre +
                       ": ")
        db.execute(
            'INSERT INTO productos (nombre, precio, cantidad, moneda) VALUES (?, ?, ?, ?)',
            (nombre.lower(), precio, cantidad, moneda))
        conn.commit()
        print("Producto " + nombre + " cuyo precio es $" + str(precio) + " x" +
              str(cantidad) + ", y que se compra con " + str(moneda) +
              ", se ha cargado exitosamente")
        nombre = input(
            "Ingrese el nombre del producto:\n(No ingresar nada para terminar la carga) "
        )


def listar_productos():
    db.execute('SELECT nombre, precio, cantidad, moneda FROM productos')
    productos = db.fetchall()
    if productos:
        print("-=============================-")
        print("|Listado de productos")
        for producto in productos:
            print("|------------------------------")
            print("| Nombre: " + str(producto[0]))
            print("| Precio: $" + str(producto[1]))
            print("| Cantidad: $" + str(producto[2]))
            print("| Moneda: " + str(producto[3]))
        print("-=============================-")
    else:
        print("No hay productos")


def promedio_precios():
    db.execute('SELECT nombre, precio FROM productos')
    lista = db.fetchall()

    if lista == ():
        print("No hay productos para calcular el promedio")
    else:
        prom = promedio(lista)
        print("El precio promedio de los productos es: $" +
              str(round(prom, 2)))


def producto_mas_caro():
    db.execute('SELECT nombre, precio, cantidad, moneda FROM productos')
    productos = db.fetchall()
    mas_caro = maximo(productos)
    print("El producto más caro es " + str(mas_caro[0]) +
          " con un precio de $" + str(mas_caro[1]) + " en " + mas_caro[3])


def producto_mas_barato():
    db.execute('SELECT nombre, precio, cantidad, moneda FROM productos')
    productos = db.fetchall()
    mas_barato = minimo(productos)
    print("El producto más barato es " + str(mas_barato[0]) +
          " con un precio de $" + str(mas_barato[1]) + " en " + mas_barato[3])


def info_sobre_producto(info):
    db.execute('SELECT nombre, precio, cantidad, moneda FROM productos')
    productos = db.fetchall()
    contador = 0
    for prod in productos:
        for i in range(len(prod)):
            if prod[i] == info.lower():
                contador += 1
                print("|------------------------------")
                print("| Nombre: " + str(prod[0]))
                print("| Precio: $" + str(prod[1]))
                print("| Cantidad: $" + str(prod[2]))
                print("| Moneda: " + str(prod[3]))
                print("|------------------------------")

    if contador == 0:
        print("No se encontró el producto :/")


def esperar_input():
    input("\nPresione Enter para continuar...")
    print("\n")


def menu():
    opcion = ""
    while opcion != "g":
        print(logo)
        print("¡Bienvenido a la pizzería Pyzza!")
        print("\ta) Cargar producto")
        print("\tb) Listar productos")
        print("\tc) Mostrar información sobre un producto")
        print("\td) Calcular precio promedio")
        print("\te) Producto más caro")
        print("\tf) Producto más barato")
        print("\tg) Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == 'a':
            cargar_producto()
        elif opcion == 'b':
            listar_productos()
            esperar_input()
        elif opcion == 'c':
            info = str(input("Ingrese el producto a buscar: "))
            info_sobre_producto(info)
            esperar_input()
        elif opcion == 'd':
            promedio_precios()
            esperar_input()
        elif opcion == 'e':
            producto_mas_caro()
            esperar_input()
        elif opcion == 'f':
            producto_mas_barato()
            esperar_input()
        elif opcion == 'g':
            print("¡Gracias por usar el sistema del comercio! ¡Hasta luego!")
        else:
            print(
                "Opción no válida, por favor seleccione una opción del menú.")
            esperar_input()


# Ejecutar el menú
menu()

# Cerrar la conexión a la base de datos al finalizar el programa
conn.close()
