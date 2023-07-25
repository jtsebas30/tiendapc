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
        valores = (id,)
        #print(sql%valores)
        cursor = db.cursor()
        cursor.execute(sql,valores)
        data = cursor.fetchall()
        cursor.close()

        return data
    except (Exception,psycopg2.DatabaseError) as error:
        db.close()
        print("Error:",error)
        return None

def validar_correo(correo):
    try:
        sql = "SELECT * FROM CLIENTE WHERE CORREO=%s"
        valores = (correo,)
        print(sql%valores)
        cursor = db.cursor()
        cursor.execute(sql, valores)
        data = cursor.fetchall()
        cursor.close()

        return data
    except (Exception, psycopg2.DatabaseError) as error:
        db.close()
        print("Error:", error)
        return None

def validar_userxcedula(cedula):
    try:
        sql = "SELECT * FROM CLIENTE WHERE CEDULA=%s"
        valores = (cedula,)
        print(sql%valores)
        cursor = db.cursor()
        cursor.execute(sql, valores)
        data = cursor.fetchall()
        cursor.close()

        return data
    except (Exception, psycopg2.DatabaseError) as error:
        db.close()
        print("Error:", error)
        return None



def validar_user(correo,contrasenia):
    try:
        sql = "SELECT * FROM CLIENTE WHERE CORREO=%s and CONTRASENIA=%s"
        valores = (correo,contrasenia)
        cursor = db.cursor()
        cursor.execute(sql,valores)
        data = cursor.fetchall()
        cursor.close()

        return data
    except (Exception,psycopg2.DatabaseError) as error:
        db.close()
        print("Error:",error)
        return None

def agregarcestabd(idproducto,cedula,fecha,cantidad,precio):
    try:
        sql = "INSERT INTO carrito (idp,cedula,fecha,cantidad,preciototal) values " \
              "(%s,%s,%s,%s,%s)"
        valores = (idproducto,cedula,fecha,cantidad,precio)
        #print(sql % valores)
        cursor = db.cursor()
        cursor.execute(sql, valores)
        db.commit()

        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        return False

def carrito_cliente(cedula):
    try:
        sql = "SELECT PRODUCTOS.IDP,PRODUCTOS.NOMBRE,CARRITO.FECHA,CARRITO.CANTIDAD,CARRITO.PRECIOTOTAL,CARRITO.IDC FROM PRODUCTOS,CARRITO,CLIENTE WHERE PRODUCTOS.IDP=CARRITO.IDP AND CLIENTE.CEDULA=CARRITO.CEDULA AND CLIENTE.CEDULA=%s"
        valores = (cedula,)
        #print(sql % valores)
        with db.cursor() as cursor:
            cursor.execute(sql, valores)
            data = cursor.fetchall()

        return data
    except (Exception,psycopg2.DatabaseError) as error:
        db.close()
        print("Error:",error)
        return None


def pedido_exitoso(cedula,fecha,total):
    try:
        sql = "INSERT INTO factura (cedula,fecha,total) values " \
              "(%s,%s,%s)"
        valores = (cedula,fecha,total)
        #print(sql % valores)
        cursor = db.cursor()
        cursor.execute(sql, valores)
        db.commit()


        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        return False

def eliminar_carrito(cedula):
    try:
        sql = "DELETE FROM CARRITO WHERE CEDULA = %s"
        valores = (cedula,)
        #print(sql % valores)
        cursor = db.cursor()
        cursor.execute(sql, valores)
        db.commit()

        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        return False


def eliminar_producto(idc):
    try:
        sql = "DELETE FROM CARRITO WHERE IDC = %s"
        valores = (idc,)
        print(sql % valores)
        cursor = db.cursor()
        cursor.execute(sql, valores)
        db.commit()

        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        return False


def cliente_comprobantes(cedula):
    try:
        sql = "SELECT * FROM FACTURA WHERE CEDULA=%s"
        valores = (cedula,)
        #print(sql % valores)
        with db.cursor() as cursor:
            cursor.execute(sql, valores)
            data = cursor.fetchall()

        return data
    except (Exception,psycopg2.DatabaseError) as error:
        db.close()
        print("Error:",error)
        return None

def solicitud_ingreso(cliente,cedula,correo,producto,fecha):
    try:
        sql = "INSERT INTO SOLICITUD_PRESTAMO (cliente,cedula,correo,producto,fecha,estado,mensaje) values " \
              "(%s,%s,%s,%s,%s,0,'Trámite Iniciado')"
        valores = (cliente,cedula,correo,producto,fecha)
        #print(sql % valores)
        cursor = db.cursor()
        cursor.execute(sql, valores)
        db.commit()


        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        return False


def cliente_solicitudes(cedula):
    try:
        sql = "SELECT * FROM SOLICITUD_PRESTAMO WHERE CEDULA=%s"
        valores = (cedula,)
        #print(sql % valores)
        with db.cursor() as cursor:
            cursor.execute(sql, valores)
            data = cursor.fetchall()

        return data
    except (Exception,psycopg2.DatabaseError) as error:
        db.close()
        print("Error:",error)
        return None