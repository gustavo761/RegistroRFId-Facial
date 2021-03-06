import cv2
import os
import imutils

def captura(personName='0000000'):
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        faceClasif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        count = 0
        dataPath = 'C:/RegistroRfidFacial/Data'
        personPath = dataPath + '/' + personName

        if not os.path.exists(personPath):
            os.makedirs(personPath)

        while True:
            ret, frame = cap.read()
            if ret == False: break
            frame = imutils.resize(frame, width=640)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = frame.copy()

            faces = faceClasif.detectMultiScale(gray,1.3,5)

            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                rostro = auxFrame[y:y+h,x:x+w]
                rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(personPath+'/rostro_{}.jpg'.format(count),rostro)
                count = count + 1
            cv2.imshow('frame', frame)

            if count >= 100: 
                break

        cap.release()
        cv2.destroyAllWindows()
    except:
        print("No se pudo capturar rostros")
#captura('Prueba')