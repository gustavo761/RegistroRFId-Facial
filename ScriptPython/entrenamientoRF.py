import cv2
import os
import numpy as np

def entrenar():
    dataPath = 'D:/Electronica/ControlAcceso/Data'
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
    print('Entrenamiendo completado')

