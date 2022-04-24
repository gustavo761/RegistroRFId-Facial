import serial
from serial.tools import list_ports
import time

puerto = serial.Serial()

# Obtener puerto COM  
def verificarSerial():    
    for i, j, k in list_ports.comports():
        return i
    return False

# Inicializar comunicacion
def iniciarComunicacion():
    try:
        puerto.port = verificarSerial()
        puerto.baudrate = 9600
        puerto.timeout = 0.1
        puerto.open()
        print("puerto iniciado")
    except:
        print("Lector no conectado")

# Lectura de datos del puerto serial
def lecturaDatos():
    if puerto.inWaiting() > 0:
        return puerto.readline().decode('ascii').replace('\r\n','')
    time.sleep(0.1)
    return False

def finalizarComunicacion():
    puerto.close()
    print("Comunicacion finalizada")

def limpiarBufferEntrada():
    try:
        puerto.flushInput()
    except:
        print("Error al limpiar buffer")

