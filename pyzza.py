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

# crear la tabla de pizzas si no existe
db.execute('''
CREATE TABLE IF NOT EXISTS pizzas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    cantidad INT NOT NULL,
    moneda TEXT NOT NULL
)
''')
conn.commit()


# promedio hace el toma una lista de pizzas y retorna el promedio (prod[1] es el precio)
def promedio(lista):
    suma = 0
    for prod in lista:
        suma += prod[1]
    return suma / len(lista)


# maximo calcula la pizza de maximo precio de una lista de pizzas
def maximo(pizzas):
    # inicializar el mayor como el menor valor posible
    precio_mayor = 0
    mayor = ["", 0]

    # recorrer la lista y actualizar el valor del mayor si encontramos un valor mayor (elemento[1] es el precio)
    for elemento in pizzas:
        if elemento[1] > precio_mayor:
            mayor = elemento
            precio_mayor = elemento[1]

    return mayor


# minimo calcula la pizzas de maximo precio de una lista de pizzas
def minimo(pizzas):
    # inicializar el menor como el mayor valor posible
    precio_menor = 9999999999999999999
    menor = ["", 0]

    # recorrer la lista y actualizar el valor del menor si encontramos un valor menor (elemento[1] es el precio)
    for elemento in pizzas:
        if elemento[1] < precio_menor:
            menor = elemento
            precio_menor = elemento[1]

    return menor


# cargar_pizzas pide el ingreso de pizzas y sus características hasta que nombre sea vacío
def cargar_pizzas():
    nombre = input("Ingrese el nombre de la pizza: ")
    while nombre != "":
        precio = float(input("Ingrese el precio de " + nombre + ": "))
        cantidad = int(input("Ingrese la cantidad de " + nombre + ": "))
        moneda = input("Ingrese la criptomoneda con la que pagar " + nombre +
                       ": ")

        # insertar datos en la db
        db.execute(
            'INSERT INTO pizzas (nombre, precio, cantidad, moneda) VALUES (?, ?, ?, ?)',
            (nombre.lower(), precio, cantidad, moneda))
        conn.commit()

        # mostrar datos cargados
        print("Pizza " + nombre + " cuyo precio es $" + str(precio) + " x" +
              str(cantidad) + ", y que se compra con " + str(moneda) +
              ", se ha cargado exitosamente")
        print("\n[No ingresar nada si quiere terminar la carga]")
        nombre = input(
            "Ingrese el nombre de la pizza: "
        )


# listar_pizzas genera una lista formateada de todos los pizzas y sus características
def listar_pizzas():
    # tomar datos en la db
    db.execute('SELECT nombre, precio, cantidad, moneda FROM pizzas')
    pizzas = db.fetchall()

    # verifico si hay pizzas
    if pizzas:
        print("-=============================-")
        print("| Listado de pizzas")
        for pizza in pizzas:
            print("|------------------------------")
            print("| Nombre: " + str(pizza[0]))
            print("| Precio: $" + str(pizza[1]))
            print("| Cantidad: $" + str(pizza[2]))
            print("| Moneda: " + str(pizza[3]))
        print("-=============================-")
    else:
        print("No hay pizzas cargadas")


# promedio_precios devuelve un string de los promedios de los precios de todos las pizzas
def promedio_precios():
    # tomar datos en la db
    db.execute('SELECT nombre, precio FROM pizzas')
    lista = db.fetchall()

    # checkeo si la lista está vacía
    if lista == ():
        return "No hay pizzas para calcular el promedio"
    else:
        prom = promedio(lista)
        salida = ("El precio promedio de las pizzas es: $" +
                  str(round(prom, 2)))
        return salida


# pizza_mas_cara devuelve el mas caro de todas las pizzas
def pizza_mas_cara():
    # tomar datos en la db
    db.execute('SELECT nombre, precio, cantidad, moneda FROM pizzas')
    pizzas = db.fetchall()

    # calculo el máximo de la lista
    mas_caro = maximo(pizzas)
    salida = ("La pizza más cara es " + str(mas_caro[0]) +
              " con un precio de $" + str(mas_caro[1]) + " en " + mas_caro[3])
    return salida


# pizza_mas_barata devuelve el mas barato de todas las pizzas
def pizza_mas_barata():
    # tomar datos en la db
    db.execute('SELECT nombre, precio, cantidad, moneda FROM pizzas')
    pizzas = db.fetchall()

    # calculo el minimo de la lista
    mas_barato = minimo(pizzas)
    salida = ("La pizza más barata es " + str(mas_barato[0]) +
              " con un precio de $" + str(mas_barato[1]) + " en " +
              mas_barato[3])
    return salida


# info_sobre_pizza devuelve la información sobre una pizza de manera formateada
def info_sobre_pizza(info):
    # tomar datos en la db
    db.execute('SELECT nombre, precio, cantidad, moneda FROM pizzas')
    pizzas = db.fetchall()
    salida = []

    # cuento la cantidad de pizzas encontradas
    contador = 0

    # itero pizzas
    for pizza in pizzas:
        # itero cada característica
        for i in range(len(pizza)):
            # si la característica es igual a lo ingresado, se devuelve la información sobre esa pizza
            if str(pizza[i]).lower() == info.lower():
                salida.append(pizza)
                contador += 1

    return salida, contador


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
        print("\ta) Cargar pizza")
        print("\tb) Listar pizzas")
        print("\tc) Mostrar información sobre una pizza")
        print("\td) Calcular precio promedio")
        print("\te) Pizza más cara")
        print("\tf) Pizza más barata")
        print("\tg) Salir")

        # analisis de opciones ingresadas
        opcion = input("\nSeleccione una opción: ").lower()
        if opcion == 'a':
            cargar_pizzas()
        elif opcion == 'b':
            listar_pizzas()
            esperar_input()
        elif opcion == 'c':
            info = str(input("Ingrese la característica a buscar: "))

            lista, contador = info_sobre_pizza(info)
            # compruebo si la lista esta vacía
            if (lista == "") or (contador == 0):
                print("\tNo se encontró una pizza con esa característica")
            else:
                # itero cada pizza encontrada
                for i in lista:
                    print("|------------------------------")
                    print("| Nombre: " + str(i[0]))
                    print("| Precio: $" + str(i[1]))
                    print("| Cantidad: $" + str(i[2]))
                    print("| Moneda: " + str(i[3]))
                    print("|------------------------------")
                print("\n¡Se han encontrado " + str(contador) + " pizza(s)!")
            esperar_input()
        elif opcion == 'd':
            print(promedio_precios())
            esperar_input()
        elif opcion == 'e':
            print(pizza_mas_cara())
            esperar_input()
        elif opcion == 'f':
            print(pizza_mas_barata())
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
