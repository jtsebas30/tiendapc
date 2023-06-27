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
    except:
        db.close()
        return False


