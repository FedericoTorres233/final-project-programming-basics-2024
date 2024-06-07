import sqlite3

# conectarse a la base de datos SQLite
conn = sqlite3.connect('pyzza.db')
db = conn.cursor()

# logo
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

# crear la tabla de productos si no existe
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


# promedio hace el toma una lista de productos y retorna el promedio (prod[1] es el precio)
def promedio(lista):
    suma = 0
    for prod in lista:
        suma += prod[1]
    return suma / len(lista)


# maximo calcula el producto de maximo precio de una lista de productos
def maximo(productos):
    # inicializar el mayor como el menor valor posible
    precio_mayor = 0
    mayor = ["", 0]

    # recorrer la lista y actualizar el valor del mayor si encontramos un valor mayor (elemento[1] es el precio)
    for elemento in productos:
        if elemento[1] > precio_mayor:
            mayor = elemento
            precio_mayor = elemento[1]

    return mayor


# minimo calcula el producto de maximo precio de una lista de productos
def minimo(productos):
    # inicializar el menor como el mayor valor posible
    precio_menor = 9999999999999999999
    menor = ["", 0]

    # recorrer la lista y actualizar el valor del menor si encontramos un valor menor (elemento[1] es el precio)
    for elemento in productos:
        if elemento[1] < precio_menor:
            menor = elemento
            precio_menor = elemento[1]

    return menor


# cargar_producto pide el ingreso de productos y sus características hasta que nombre sea vacío
def cargar_producto():
    nombre = input("Ingrese el nombre del producto: ")
    while nombre != "":
        precio = float(input("Ingrese el precio de " + nombre + ": "))
        cantidad = int(input("Ingrese la cantidad de " + nombre + ": "))
        moneda = input("Ingrese la criptomoneda con la que pagar " + nombre +
                       ": ")

        # insertar datos en la db
        db.execute(
            'INSERT INTO productos (nombre, precio, cantidad, moneda) VALUES (?, ?, ?, ?)',
            (nombre.lower(), precio, cantidad, moneda))
        conn.commit()

        # mostrar datos cargados
        print("Producto " + nombre + " cuyo precio es $" + str(precio) + " x" +
              str(cantidad) + ", y que se compra con " + str(moneda) +
              ", se ha cargado exitosamente")
        nombre = input(
            "Ingrese el nombre del producto:\n(No ingresar nada para terminar la carga) "
        )


# listar_productos genera una lista formateada de un producto y sus características
def listar_productos():
    # tomar datos en la db
    db.execute('SELECT nombre, precio, cantidad, moneda FROM productos')
    productos = db.fetchall()

    # verifico si hay productos
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


# promedio_precios devuelve el promedio de los precios de todos los productos
def promedio_precios():
    # tomar datos en la db
    db.execute('SELECT nombre, precio FROM productos')
    lista = db.fetchall()

    # checkeo si la lista está vacía
    if lista == ():
        print("No hay productos para calcular el promedio")
    else:
        prom = promedio(lista)
        print("El precio promedio de los productos es: $" +
              str(round(prom, 2)))


# producto_mas_caro devuelve el mas caro de todos los productos
def producto_mas_caro():
    # tomar datos en la db
    db.execute('SELECT nombre, precio, cantidad, moneda FROM productos')
    productos = db.fetchall()

    # calculo el máximo de la lista
    mas_caro = maximo(productos)
    print("El producto más caro es " + str(mas_caro[0]) +
          " con un precio de $" + str(mas_caro[1]) + " en " + mas_caro[3])


# producto_mas_caro devuelve el mas barato de todos los productos
def producto_mas_barato():
    # tomar datos en la db
    db.execute('SELECT nombre, precio, cantidad, moneda FROM productos')
    productos = db.fetchall()

    # calculo el minimo de la lista
    mas_barato = minimo(productos)
    print("El producto más barato es " + str(mas_barato[0]) +
          " con un precio de $" + str(mas_barato[1]) + " en " + mas_barato[3])


# info_sobre_producto devuelve la información sobre un producto de manera formateada
def info_sobre_producto(info):
    # tomar datos en la db
    db.execute('SELECT nombre, precio, cantidad, moneda FROM productos')
    productos = db.fetchall()

    # el contador se utiliza para comprobar si se encontró un producto
    contador = 0

    # itero productos
    for prod in productos:
        # itero cada característica
        for i in range(len(prod)):
            # si la característica es igual a lo ingresado, se devuelve la información sobre ese producto
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


# genera el prompt para volver a mostrar el menú
def esperar_input():
    input("\nPresione Enter para continuar...")
    print("\n")


# inicializo el menú
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

        # analisis de opciones ingresadas
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


# ejecutar el menú
menu()

# cerrar la conexión a la db por seguridad
conn.close()
