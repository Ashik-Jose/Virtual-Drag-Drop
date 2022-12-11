import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

cap.set(3,980)
cap.set(4,520)

detector = HandDetector(detectionCon=0.8)

while True:
    success,img = cap.read()
    lis = detector.findHands(img)
    #lmList, _ = detector.findHands(img)
    print(lis.lmList)


    cv2.imshow("Image",img)
    cv2.waitKey(1)