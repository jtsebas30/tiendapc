import psycopg2

db = psycopg2.connect(host="localhost", database="tienda", user="postgres", password="1234")

def nuevousuario(cedula,nombre,apellido,provincia,domicilio,correo,contrasenia):
    try:
        sql = "INSERT INTO cliente (cedula,nombre,apellido,provincia,direccion,correo,contrasenia) values " \
              "(%s,%s,%s,%s,%s,%s,%s)"
        valores = (cedula, nombre, apellido, provincia, domicilio, correo,contrasenia)
        #print(sql % valores)
        cursor = db.cursor()
        cursor.execute(sql, valores)
        db.commit()
        db.close()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        return False


def verproductos():
    try:
        sql = "SELECT * FROM PRODUCTOS"
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()

        return data
    except (Exception,psycopg2.DatabaseError) as error:
        db.close()
        print("Error:",error)
        return None

def verproductos_detalle(id):
    try:
        sql = "SELECT * FROM PRODUCTOS WHERE IDP=%s"
        valores = (id)
        cursor = db.cursor()
        cursor.execute(sql,valores)
        data = cursor.fetchall()
        cursor.close()

        return data
    except (Exception,psycopg2.DatabaseError) as error:
        db.close()
        print("Error:",error)
        return None



