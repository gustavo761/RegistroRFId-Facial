from glob import glob
import cv2
import os

dataPath = 'D:/Electronica/ControlAcceso/Data'
imagePaths = os.listdir(dataPath)
#print('imagePaths+',imagePaths)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Leyendo el modelo
face_recognizer.read('modeloLBPHFace.xml')

#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

faceClasif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

def recFacial(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()
    retorno = [-1, frame,""]
    faces = faceClasif.detectMultiScale(gray,1.3,5)
    result = 0
    for (x,y,w,h) in faces:
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        result = face_recognizer.predict(rostro)
        #cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
        retorno[0] = result[0]
        # LBPH
        if result[1] < 57:
            frame = cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),1,1.1,(0,255,0),1,cv2.LINE_AA)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            retorno[2] = imagePaths[result[0]]
        else:
            print(-1,"No registrado")
            retorno[2] = "NO REGISTRADO"
        retorno[1] = frame
    return retorno 
'''
        else:
            frame = cv2.putText(frame,'desconocido',(x,y-5),1,1.3,(0,0,255),1,cv2.LINE_AA)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
'''