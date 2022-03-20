from ast import AsyncFunctionDef
import connArduino as cA
import capturaRostro as cR
import entrenamientoRF as eRF
import reconocimientoFacial as rF
import validaciones as valid
import connBD as cBD
from tkinter import messagebox, ttk
from tkinter import messagebox as MessageBox
import tkinter as tk
import cv2
import imutils
from PIL import Image
from PIL import ImageTk

# pasar parametros con command=lambda:funcion()

def contarCoincidencias(nuevoValor):
    global valorAnterior
    global contador
    if nuevoValor != -1:
        if valorAnterior == nuevoValor:
            contador = contador + 1
            if contador > 9:
                contador = 0
                print("Identidad verificada")
        else:
            contador = 0
        valorAnterior = nuevoValor
    else:
        contador = 0
        valorAnterior = -2
    #print("Valores en contar coincidencias: ", nuevoValor, valorAnterior)

def visualizar():
    global cap
    ret, frame = cap.read()
    if ret == True:
        frame = imutils.resize(frame, width=410)
        #frame = rF.recFacial(frame)
        resultado = rF.recFacial(frame)
        contarCoincidencias(resultado[0])
        labelNombre.set(resultado[2])
        frame = cv2.cvtColor(resultado[1], cv2.COLOR_BGR2RGB)

        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar)

def iniciarVideo():
    global cap
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    visualizar()

def detenerVideo():
    global cap
    cap.release()

def cambioEstado():
    global rfidPrincipal
    rfidPrincipal = not rfidPrincipal
    lectorRFID()

def lectorRFID():
    global rfidPrincipal
    if rfidPrincipal:
        idRfid = cA.lecturaDatos()
        if idRfid:
            print("codigo registrado principal "+ idRfid)
        principal.after(100,lectorRFID)

def abrirRegistrar():
    cambioEstado()
    detenerVideo()
    def registrarUsuario():
        mensaje=""
        verificado = True
        if not valid.verificarNombre(edtNombresEntry.get()):
            mensaje = mensaje + "El nombre solo debe contener letras\n"
            verificado = False
        if not valid.verificarNombre(edtApellidosEntry.get()):
            mensaje = mensaje + "El apellido solo debe contener letras\n"
            verificado = False
        if not valid.verificarCarnet(edtCarnetEntry.get()):
            mensaje = mensaje + "El carnet solo debe contener numeros\n"
            verificado = False
        if len(lblRFIDlabel.get()) == 0:
            mensaje = mensaje + "Debe acercar una tarjeta al lector\n"
            verificado = False
        if verificado:
            print("Hacer consulta")
            if cBD.consultaBDCarnet(edtCarnetEntry.get()):
                print("consulta update")
                if MessageBox.askquestion("Actualizar",'''El número de carnet ya se encuentra registrado 
                    desea actualizar la información ingresada?''') == "yes":
                    query = f'update USUARIO set nombre="{edtNombresEntry.get()}", apellido="{edtApellidosEntry.get()}",carnet={edtCarnetEntry.get()},rfid="{lblRFIDlabel.get()}" where carnet={edtCarnetEntry.get()}'
                    cBD.updateBD(query)
                    cBD.insertarCelular(edtCarnetEntry.get(),edtCelularEntry.get())
            else:
                if cBD.consultaBDRfid(lblRFIDlabel.get()):
                    MessageBox.showinfo("Tarjeta Registrada","La tarjeta ya ha sido registrada, seleccione otra")
                else:
                    cBD.insertarUsuario(edtCarnetEntry.get(), edtNombresEntry.get(),edtApellidosEntry.get(),"Docente","Tarde",lblRFIDlabel.get())
                    cBD.insertarCelular(edtCarnetEntry.get(),edtCelularEntry.get())
                    print("Usuario registrado")
            
        else:
            MessageBox.showinfo("ERROR",mensaje)
    
    def editar():
        print("hola mundo editar")
        if valid.verificarCarnet(edtCarnetEntry.get()):
            # query con carnet
            consulta = cBD.consultaBD(f'select * from USUARIO where carnet={edtCarnetEntry.get()}')
            print(consulta)
            if consulta[0] != 0:
                edtNombresEntry.set(consulta[1][0]["NOMBRE"])
                edtApellidosEntry.set(consulta[1][0]["APELLIDO"])
                lblRFIDlabel.set(consulta[1][0]["RFID"])
                nroCelular = cBD.buscarCelular(edtCarnetEntry.get())
                edtCelularEntry.set(nroCelular["numero"])

                print('editar campos')
            else:
                MessageBox.showinfo("ERROR",'CARNET NO REGISTRADO')

    def capturaRostro():
        if valid.verificarCarnet(edtCarnetEntry.get()):
            #verificar la lista de carnets en la carpeta data
            if cBD.consultaBDCarnet(edtCarnetEntry.get()):
                MessageBox.showinfo("ERROR","EL USUARIO YA REGISTRO SU ROSTRO EN EL SISTEMA")
                print("Carnet ya registrado")
            else:
                cR.captura(edtCarnetEntry.get())
                MessageBox.showinfo("INFORMACIÓN","DEBE REINICIAR EL PROGRAMA PARA APLICAR LOS CAMBIOS")
                print("Reiniciar el programa despues de entrenar")
        else:
            MessageBox.showinfo("ERROR","ANTES DEBE REGISTRAR EL USUARIO")
        print("hola mundo captura")
    
    def iniciarRFID():
        global rfidRegistrar
        rfidRegistrar = not rfidRegistrar
        #cA.iniciarComunicacion()
        lecturaRFID()

    def lecturaRFID():
        global rfidRegistrar
        if rfidRegistrar:
            idRfid = cA.lecturaDatos()
            if idRfid:
                lblRFIDlabel.set(idRfid)
                print("codigo registrado registro "+ idRfid)
            registrar.after(100,lecturaRFID)
    
    def volverRegistrar():
        global rfidRegistrar
        rfidRegistrar = not rfidRegistrar
        #cA.finalizarComunicacion()
        cambioEstado()
        iniciarVideo()
        registrar.destroy()

    registrar = tk.Toplevel(principal)
    registrar.title("REGISTRAR")
    registrar.geometry("500x500"+"+100+100")
    registrar.resizable(height=False, width=False)
    fondoP = tk.PhotoImage(file="fondos/registro.png")
    labelFondo = tk.Label(registrar, image=fondoP)
    labelFondo.place(x=0,y=0)
    edtNombresEntry = tk.StringVar()
    edtNombres = tk.Entry(registrar,
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0,
        textvariable=edtNombresEntry
    )
    edtNombres.place(x=215,y=90)
    edtApellidosEntry = tk.StringVar()
    edtApellidos = tk.Entry(registrar,
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0,
        textvariable=edtApellidosEntry
    )
    edtApellidos.place(x=215,y=145)
    edtCarnetEntry = tk.StringVar()
    edtCarnet = tk.Entry(registrar,
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0,
        textvariable=edtCarnetEntry
    )
    edtCarnet.place(x=215,y=205)
    lblRFIDlabel = tk.StringVar()
    lblRFID = tk.Label(registrar,
        text = "prueba",
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0,
        textvariable=lblRFIDlabel
    )
    lblRFID.place(x=215,y=260)
    edtCelularEntry = tk.StringVar()
    edtCelular = tk.Entry(registrar,
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0,
        textvariable=edtCelularEntry
    )
    edtCelular.place(x=215,y=315)
    btnRegistrar = tk.Button(registrar,
        text="REGISTRAR", 
        command=registrarUsuario, 
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0
    )
    btnRegistrar.place(x=90,y=420)
    btnCaptura = tk.Button(registrar,
        text="CAPTURAR ROSTRO", 
        command=capturaRostro, 
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0
    )
    btnCaptura.place(x=95,y=365)
    btnEditar = tk.Button(registrar,
        text="EDITAR", 
        command=editar, 
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0
    )
    btnEditar.place(x=345,y=365)
    btnVolver = tk.Button(registrar,
        text="VOLVER", 
        command=volverRegistrar, 
        bg="#ff1616",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0
    )
    btnVolver.place(x=320,y=420)
    registrar.after(2000,iniciarRFID)
    registrar.transient(master=principal)
    registrar.grab_set()
    principal.wait_window(registrar)
    
def abrirReporte():
    cambioEstado()
    detenerVideo()
    def volverGenerar():
        cA.limpiarBufferEntrada()
        cambioEstado()
        iniciarVideo()
        reporte.destroy()

    reporte = tk.Toplevel(principal)
    reporte.title("GENERAR REPORTE")
    reporte.geometry("500x500"+"+100+100")
    reporte.resizable(height=False, width=False)
    fondoP = tk.PhotoImage(file="fondos/generarReporte.png")
    labelFondo = tk.Label(reporte, image=fondoP)
    labelFondo.place(x=0,y=0)
    meses = ['Elija un mes','Enero','Febrero','Marzo','Abril','Mayo',
        'Junio','Julio','Agosto','Septiembre',
        'Octubre','Noviembre','Diciembre']
    edtCarnet = tk.Entry(reporte,
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0
    )
    edtCarnet.place(x=215,y=120)
    cmbMes = ttk.Combobox(reporte,
        font=("Comic Sans MS", 13, "bold"),
        values=meses,
        state="readonly"
    )
    cmbMes.place(x=215,y=183)
    cmbMes.current(0)
    edtAnio = tk.Entry(reporte,
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0
    )
    edtAnio.place(x=215,y=250)
    btnGenerar = tk.Button(reporte,
        text="REPORTE", 
        command="", 
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0
    )
    btnGenerar.place(x=210,y=333)
    btnVolver = tk.Button(reporte,
        text="VOLVER", 
        command=volverGenerar, 
        bg="#ff1616",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0
    )
    btnVolver.place(x=220,y=407)
    reporte.transient(master=principal)
    reporte.grab_set()
    principal.wait_window(reporte)

def abrirEntrenar():
    cambioEstado()
    detenerVideo()
    def volverEntrenar():
        cA.limpiarBufferEntrada()
        cambioEstado()
        iniciarVideo()
        entrenar.destroy()

    entrenar = tk.Toplevel(principal)
    entrenar.title("ENTRENAR")
    entrenar.geometry("500x500"+"+100+100")
    entrenar.resizable(height=False, width=False)
    fondoP = tk.PhotoImage(file="fondos/entrenar.png")
    labelFondo = tk.Label(entrenar, image=fondoP)
    labelFondo.place(x=0,y=0)
    btnEntrenar = tk.Button(entrenar,
        text="ENTRENAR", 
        command=eRF.entrenar, 
        bg="#004aad",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0
    )
    btnEntrenar.place(x=90,y=420)
    btnVolver = tk.Button(entrenar,
        text="VOLVER", 
        command=volverEntrenar, 
        bg="#ff1616",
        fg="white",
        relief="flat",
        font=("Comic Sans MS", 13, "bold"),
        bd=0
    )
    btnVolver.place(x=320,y=420)
    entrenar.transient(master=principal)
    entrenar.grab_set()
    principal.wait_window(entrenar)

def salir():
    cA.finalizarComunicacion()
    detenerVideo()
    cBD.desconectarBD()
    principal.destroy()

# ----------------------------- main 

principal = tk.Tk()
principal.geometry("1200x600")
principal.resizable(height=False, width=False)
fondoP = tk.PhotoImage(file="fondos/principal.png")
labelFondo = tk.Label(principal, image=fondoP)
labelFondo.place(x=0,y=0)
labelNombre = tk.StringVar()
lblModoRegistro = tk.Label(principal,
    text="VENTANA PRINCIPAL",
    bg="#004aad",
    fg="white",
    relief="flat",
    font=("Comic Sans MS", 15, "bold"),
    bd=0,
    textvariable=labelNombre
)
lblModoRegistro.place(x=320,y=160)

btnRe = tk.Button(principal,
    text="REGISTRAR", 
    command=abrirRegistrar, 
    bg="#004aad",
    fg="white",
    relief="flat",
    font=("Comic Sans MS", 15, "bold"),
    bd=0
)
btnRe.place(x=570,y=260)

btnRep = tk.Button(principal,
    text="REPORTE",
    command=abrirReporte, 
    bg="#004aad",
    fg="white",
    relief="flat",
    font=("Comic Sans MS", 15, "bold"),
    bd=0
)
btnRep.place(x=580,y=325)

btnEn = tk.Button(principal,
    text="ENTRENAR", 
    command=abrirEntrenar, 
    bg="#004aad",
    fg="white",
    relief="flat",
    font=("Comic Sans MS", 15, "bold"),
    bd=0
)
btnEn.place(x=570,y=390)

btnSalir = tk.Button(principal,
    text="SALIR", 
    command=salir, 
    bg="#004aad",
    fg="white",
    relief="flat",
    font=("Comic Sans MS", 15, "bold"),
    bd=0
)
btnSalir.place(x=590,y=455)

lblVideo = tk.Label(principal)
lblVideo.place(x=130,y=225)

cap = None
rfidPrincipal = True
rfidRegistrar = False
valorAnterior = -1
contador = 0
def iniciar():
    if cA.verificarSerial():
        if cBD.iniciarBD():
            principal.after(1000,cA.iniciarComunicacion)
            principal.after(1500,lectorRFID)
            principal.after(2000,iniciarVideo) 
            principal.mainloop()
        else:
            respuestaBD = MessageBox.askquestion(
                "Error",
                "El servidor de Base de Datos no se encuentra en línea"+
                "¿Desea reintentar?"
            )
            if respuestaBD:
                iniciar()
            else:
                principal.destroy()
    else:
        respuesta = MessageBox.askquestion(
            "Error",
            "El lector de tarjetas no se encuentra conectado\n"+
            "¿Deser reintentar?"
        )
        if respuesta == "yes":
            iniciar()
        else:
            principal.destroy()

if __name__ == "__main__":
    #iniciar()
    principal.after(1000,cA.iniciarComunicacion)
    principal.after(1500,lectorRFID)
    principal.after(2000,iniciarVideo)
    principal.after(2500,cBD.iniciarBD)
    principal.mainloop()

