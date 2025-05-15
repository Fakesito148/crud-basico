import mysql.connector
from tabulate import tabulate
from dotenv import load_dotenv
import os

load_dotenv()

conexion = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conexion.cursor()
ver_tabla = "SELECT * FROM productos"
añadir_producto = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"

while True:
    print("-----MENU-----")
    print("1.- Insertar nuevos datos")
    print("2.- Ver prductos")
    print("3.- Actualizar producto")



    cursor.execute(ver_tabla)
    filas = cursor.fetchall()
    table = tabulate(
        filas,
        headers = ["id", "Producto", "Precio", "Stock"],
        tablefmt = "fancy_grid",
        numalign="right",
        stralign="center"
    )




    eleccion = int(input("Ingrese eleccion: "))

    if eleccion == 1:
        producto = input("Nombre del producto: ")
        precio = float(input("Precio: "))
        stock = int(input("Stock disponible: "))
        valores = (producto, precio, stock)
        cursor.execute(añadir_producto, valores)
        conexion.commit()
    elif eleccion == 2:
        print(table)
    elif eleccion == 3:
        print("¿Que desea actualizar?")
        print("1.- Precio")
        print("2.- Nombre")
        print("3.- Stock")
        print(table)
        eleccion_actualizar = int(input("Eleccion: "))

        id_producto = int(input("Id del producto a actualizar: "))

    #Actualizar el precio
        if eleccion_actualizar == 1:
            try:
                nuevo_precio = float(input("Nuevo precio: "))
                cursor.execute("UPDATE productos SET precio = %s WHERE id = %s", (nuevo_precio, id_producto))
                conexion.commit()
                print("Precio del producto actualizado :)")
            except ValueError:
                print("Se debe ingresar un numero valido para el precio")
            except mysql.connector.Error as error:
                print(f"Error al actualizar el precio: {error}")

    #Actualizar nombre del producto
        elif eleccion_actualizar == 2:

            try:
                nuevo_nombre = input("Nombre: ")
                cursor.execute("UPDATE productos SET nombre = %s WHERE id = %s",(nuevo_nombre, id_producto))
                conexion.commit()
                print("Nombre actualizado con exito :)")
            except ValueError:
                print("Se debe ingresar un valor de tipo caracter, no de otro tipo")
            except mysql.connector.Error as error:
                print(f"Error al actualizar el nombre: {error}")


    #Actualizar stock del producto
        elif eleccion_actualizar == 3:
            stock_actualizado = int(input("Nuevo Stock: "))
            cursor.execute("UPDATE productos SET stock = %s WHERE id = %s", (stock_actualizado,id_producto))
            conexion.commit()

    else:
        print("Opcion no valida")
        break
    






cursor.close()
conexion.close()