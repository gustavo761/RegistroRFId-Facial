import pymysql.cursors

conn = None

def iniciarBD():
    global conn
    try:
        conn = pymysql.connect(
                host='192.168.100.32',
                user='director',
                password='jmpadmin',
                db='joseManuelPando',
                cursorclass=pymysql.cursors.DictCursor
            )
        print("Base de datos conectada")
        return True
    except:
        print("no hay base de datos")
        return False

def consultaBD(query):
    global conn
    respuesta = []
    cursor = conn.cursor()
    resultado = cursor.execute(query)
    for k in cursor:
        respuesta.append(k)
    cursor.close()
    return (resultado,respuesta)

def consultaBDCarnet(carnet):
    global conn
    cursor = conn.cursor()
    resultado = cursor.execute(f"select carnet from USUARIO where carnet={carnet}")
    cursor.close()
    if resultado == 0:
        return False
    else:
        return True

def consultaBDRfid(rfid):
    global conn
    cursor = conn.cursor()
    resultado = cursor.execute(f'select rfid from USUARIO where rfid="{rfid}"')
    cursor.close()
    if resultado == 0:
        return False
    else:
        return True

def insertarUsuario(carnet,nombre,apellido,tipo,turno,rfid):
    global conn
    cursor = conn.cursor()
    query = f'''insert into USUARIO values(
        {carnet},"{nombre}","{apellido}","{tipo}","{turno}","{rfid}")'''
    cursor.execute(query)
    cursor.close()
    conn.commit()
    print("usuario insertado")

def insertarCelular(carnet,celular):
    global conn
    print("Registrando celular")
    cursor = conn.cursor()
    if cursor.execute(f"select * from CELULAR where carnet={carnet}") == 0:
        query = f"insert into CELULAR values ({carnet}, {celular})"
        cursor.execute(query)
    cursor.close()
    conn.commit()
    print("Celular registrado")

def buscarCelular(carnet):
    global conn
    cursor = conn.cursor()
    resultado = cursor.execute(f'select numero from CELULAR where carnet={carnet}')
    respuesta = ""
    if resultado != 0:
        respuesta = cursor.fetchone()
    cursor.close()
    return respuesta

def listarNombres():
    global conn 
    cursor = conn.cursor()
    cursor.execute("select carnet, nombre || apellido from USUARIO")
    


def updateBD(query):
    global conn
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()
    print("Datos actualizados")

def desconectarBD():
    global conn
    conn.close()
    print("Base de datos desconectada")


#iniciarBD()
#desconectarBD()
