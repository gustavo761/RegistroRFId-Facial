from datetime import datetime
import os
import datosLogin as DL

def obtenerFecha():
    fecha = datetime.now().date()
    fch = f"{fecha.year}-{fecha.month}-{fecha.day}"
    return fch

def obtenerHora():
    hora = datetime.now().time()
    hr = f"{hora.hour}-{hora.minute}-{hora.second}"
    return hr

def generarCopiaSeguridad():
    print("Iniciando copia de seguridad")
    command = f"mysqldump -h 192.168.1.2 -u {DL.usuario()} -p{DL.contraseña} {DL.baseDatos()}" 
    command = command+f" > C:\RegistroRfidFacial\CopiasSeguridad\{obtenerFecha()}-{obtenerHora()}.sql"
    try:
        os.system(command)
    except:
        print("No se ha podido realizar la copia de seguridad")