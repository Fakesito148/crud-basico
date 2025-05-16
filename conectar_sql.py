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
añadir_producto = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"

#Funcion para añadir producto
def aniadir_productos(cursor):
    producto = input("Nombre del producto: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock disponible: "))
    valores = (producto, precio, stock)
    cursor.execute(añadir_producto, valores)
    conexion.commit()


#Funcion para ver productos

def ver_productos(cursor):
    ver_tabla = "SELECT * FROM productos"
    cursor.execute(ver_tabla)
    filas = cursor.fetchall()
    table = tabulate(
        filas,
        headers = ["id", "Producto", "Precio", "Stock"],
        tablefmt = "fancy_grid",
        numalign="right",
        stralign="center"
    )
    return table

#Funcion para actualizar

def actualizar_productos(cursor):
    print("¿Que desea actualizar?")
    print("1.- Precio")
    print("2.- Nombre")
    print("3.- Stock")

    print(ver_productos(cursor))
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

#Funcion para borrar productos

def borrar_productos(cursor):
    try:
        id_producto = int(input("Ingrese el id a borrar: "))

        validacion = input("¿Estas seguro?, Esto eliminara el producto de manera permanente (s/n): ").lower()

        if validacion == 's':
            cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto, ))
            conexion.commit()
            print("Producto eliminado con exito")
        elif validacion == 'n':
            print("Ha decidido no borrar el producto")
        else:
            print("Ingrese un valor valido")
    except ValueError:
        print("No es un valor valido, ingrese un dato de tipo entero para el id")
    except mysql.connector.Error as error:
        print(f"Error al borrar el archivo: {error}")





while True:
    print("-----MENU-----")
    print("1.- Insertar nuevos datos")
    print("2.- Ver prductos")
    print("3.- Actualizar producto")
    print("4.- Borrar Producto")

    eleccion = int(input("Ingrese eleccion: "))


        #AÑADIR PRODUCTOS
    if eleccion == 1:
        aniadir_productos(cursor)
        
        #VER PRODUCTOS
    elif eleccion == 2:
        print(ver_productos(cursor))

        #MENU DE ACTUALIZACION
    elif eleccion == 3:
       actualizar_productos(cursor)

       #BORRAR PRODUCTO
    elif eleccion == 4:
       borrar_productos(cursor)
    else:
        print("Opcion no valida")
        break

cursor.close()
conexion.close()
