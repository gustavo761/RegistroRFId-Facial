from dataclasses import asdict
from tkinter import messagebox as MessageBox
import capturaRostro as cR

def verificarNombre(cadena):
    for i in cadena:
        if (not ((i>="A" and i<="z") or i==" ")):
            return False
    return True

def verificarNumeros(cadena):
    if not cadena.isdigit():
        return False
    return True

def verificarCarnet(cadena):
    if cadena.isdigit() and len(cadena)>6 and len(cadena)<10:
        return True
    return False

def notificar(aviso):
    MessageBox.showinfo("INFORMACION",aviso)

def verificarRFID(id):
    if len(id) > 0:
        return True
    return False

def capturarRostro(carnet):
    if verificarCarnet(carnet):
        cR.captura(carnet)

def editar(carnet):
    if verificarCarnet(carnet):
        # Buscar carnet en base de datos y 
        # retornar en una tupla
        '''
        query = queribd(carnet)
        if len(query):
            return query
        else:
            print("carnet no registrado")
        '''
        return "resultado"
    else:
        print("datos invalidos")