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
        print("La base de datos no se encuentra disponible")
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
    respuesta = {}
    cursor = conn.cursor()
    cursor.execute("select carnet, nombre, apellido, rfid from USUARIO")
    for datos in cursor:
        respuesta[datos["carnet"]] = [datos["nombre"]+" "+datos["apellido"],datos["rfid"]]
    cursor.close()
    return respuesta

def updateBD(query):
    global conn
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()
    print("Datos actualizados")

def registrarMarcado(carnet,tipo,fecha,hora):
    global conn
    cursor = conn.cursor()
    query = f"select * from REGISTRO where carnet={carnet} and fecha='{fecha}'"
    respuesta = cursor.execute(query)
    if respuesta != 0:
        cursor.execute(f"update REGISTRO set horafinal='{hora}', modoregistro='{tipo}' where carnet={carnet} and fecha='{fecha}'")
        print("Hora de salida registrada")
    else:
        cursor.execute(f"insert into REGISTRO (carnet,fecha,horallegada,modoregistro) values ({carnet},'{fecha}','{hora}','{tipo}')")
        print("Hora de llegada registrada")
    cursor.close()
    conn.commit()

def desconectarBD():
    global conn
    try:
        conn.close()
        print("Base de datos desconectada")
    except:
        print("Base de datos no disponible")
    

