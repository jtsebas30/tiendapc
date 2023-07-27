import psycopg2

db = psycopg2.connect(host="localhost", database="tienda", user="postgres", password="1234")

def entendibilidad(ayudas,accedidas,errores,tiempo,fecha):
    try:
        sql = "INSERT INTO ENTENDIBILIDAD (nayudas, npagacc, nmensajeserror, tiempopaginas,fecha) values " \
              "(%s,%s,%s,%s,%s)"
        valores = (ayudas,accedidas,errores,tiempo,fecha)
        #print(sql % valores)
        cursor = db.cursor()
        cursor.execute(sql, valores)
        db.commit()

        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        return False

def efectividad(transacciones,sesiones,fecha):
    try:
        sql = "INSERT INTO EFECTIVIDAD (transacciones, sesiones,fecha) values " \
              "(%s,%s,%s)"
        valores = (transacciones,sesiones,fecha)
        #print(sql % valores)
        cursor = db.cursor()
        cursor.execute(sql, valores)
        db.commit()

        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        return False


def eficiencia(ttransaccion, nctransacciones, fecha):
    try:
        sql = "INSERT INTO EFICIENCIA (tiempocompletar, texito,fecha) values " \
              "(%s,%s,%s)"
        valores = (ttransaccion, nctransacciones, fecha)
        # print(sql % valores)
        cursor = db.cursor()
        cursor.execute(sql, valores)
        db.commit()

        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        return False
