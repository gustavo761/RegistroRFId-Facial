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
    puerto.port = verificarSerial()
    puerto.baudrate = 9600
    puerto.timeout = 0.1
    puerto.open()
    print("puerto iniciado")

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
    puerto.flushInput()
# Prueba de comunicaciones con arduino
# lectura de datos con 
'''
iniciarComunicacion()
for i in range(300):
    if puerto.inWaiting() > 0:
        print(puerto.readline().decode('ascii').replace('\r\n',''))
    time.sleep(0.01)

finalizarComunicacion()

'''
