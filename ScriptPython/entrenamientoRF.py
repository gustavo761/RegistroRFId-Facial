import cv2
import os
import numpy as np
from tkinter import messagebox as MessageBox

def entrenar():
    dataPath = 'D:\Electronica\RegistroRFId-Facial/Data'
    peopleList = os.listdir(dataPath)

    labels = []
    facesData = []
    label = 0

    for nameDir in peopleList:
        personPath = dataPath + '/' + nameDir

        for fileName in os.listdir(personPath):
            labels.append(label)
            facesData.append(cv2.imread(personPath+'/'+fileName,0))
            image = cv2.imread(personPath+'/'+fileName,0)
        label = label + 1

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    #Entrenando el reconocedor de rostros
    print('Entrenando...')
    face_recognizer.train(facesData, np.array(labels))

    #Almacenando el modelo obtenido
    face_recognizer.write('modeloLBPHFace.xml')
    MessageBox.showinfo("COMPLETADO","ENTRENAMIENTO COMPLETADO.\nCIERRE EL PROGRAMA Y VUELVA A INICIAR PARA REGISTRAR LOS CAMBIOS")
    print('Entrenamiendo completado')

