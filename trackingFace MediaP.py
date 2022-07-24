import cv2
from pyfirmata import Arduino,SERVO
from time import sleep
import mediapipe as mp

face = mp.solutions.face_detection
Face = face.FaceDetection()
mpDwaw = mp.solutions.drawing_utils

port = 'COM3'
pinH = 10
pinV = 8
board = Arduino(port)

board.digital[pinH].mode = SERVO
board.digital[pinV].mode = SERVO

def rotateServo(pin,angle):
    board.digital[pin].write(angle)
    sleep(0.015)

cap = cv2.VideoCapture(0)

positionX = 50
positionY = 70

rotateServo(pinH, positionX)
rotateServo(pinV, positionY)

while True:
    ret, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Face.process(imgRGB)
    facesPoints = results.detections
    hO, wO, _ = img.shape

    cv2.line(img,(0,int(hO/2)),(wO,int(hO/2)),(0,255,0),2)
    cv2.line(img, (int(wO / 2), 0), (int(wO / 2), hO), (0, 255, 0), 2)

    if facesPoints:
        for id, detection in enumerate(facesPoints):
            #mpDwaw.draw_detection(img, detection)
            bbox = detection.location_data.relative_bounding_box
            x,y,w,h = int(bbox.xmin*wO),int(bbox.ymin*hO),int(bbox.width*wO),int(bbox.height*hO)

            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            # centro do rosto
            xx = int(x + (x + w)) // 2
            yy = int(y + (y + h)) // 2
            cv2.circle(img, (xx, yy), 15, (0, 255, 0), cv2.FILLED)

            ctX = int(wO / 2)
            ctY = int(hO / 2)

            cv2.circle(img, (ctX, ctY), 15, (255, 0, 0), cv2.FILLED)

            #movimento eixo X
            if xx < (ctX - 50):
                positionX += 2
                rotateServo(pinH, positionX)
            elif xx > (ctX + 50):
                positionX -= 2
                rotateServo(pinH, positionX)
            # movimento eixo Y
            if yy > (ctY + 50):
                positionY += 2
                rotateServo(pinV, positionY)
            elif yy < (ctY - 50):
                positionY -= 2
                rotateServo(pinV, positionY)


    cv2.imshow('img', img)

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break



