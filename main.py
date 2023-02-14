import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)

cap.set(3,1500)
cap.set(4,980)

detector = HandDetector(detectionCon=0.8)


cx,cy,w,h = 100,100,200,200


class DragDrop():
    def __init__(self,posCenter,size=[200,200],colorR = (250,120,250)):
        self.posCenter = posCenter
        self.size = size
        self.colorR = colorR 

    def update(self,cursor):

        cx,cy = self.posCenter
        w,h = self.size

        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
            self.posCenter[0]= cursor[0]
            self.posCenter[1]= cursor[1]
            self.colorR = (0,250,0)

rectList = []
for x in range(5):
    rectList.append(DragDrop([x*250+150,150]))
            

while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    hands,img = detector.findHands(img)
    #lmList, _ = detector.findPosition(img)
    #print(hands)
    

    if hands:
        hand1=hands[0]     
        lmList1 = hand1["lmList"]     
        l1,_=detector.findDistance((lmList1[8][0],lmList1[8][1]),(lmList1[12][0],lmList1[12][1]),img=None)   
        if l1<55 :
            cursor1 = lmList1[8]
            #print(l)
            for rect in rectList:
                rect.update(cursor1)         
        else:
            for rect in rectList:
                rect.colorR = (250,120,250)
        
        if len(hands)==2:
            hand2=hands[1]
            lmList2 = hand2["lmList"]
            l2,_=detector.findDistance((lmList2[8][0],lmList2[8][1]),(lmList2[12][0],lmList2[12][1]),img=None)
            if l2<55 :
                cursor2 = lmList2[8]
            #print(l)
                for rect in rectList:    
                    rect.update(cursor2)       
                else:
                    for rect in rectList:
                        rect.colorR = (250,120,250)

    # for rect in rectList:        
    #     cx,cy = rect.posCenter
    #     w,h = rect.size
    #     cv2.rectangle(img,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),rect.colorR,cv2.FILLED)
    #     cvzone.cornerRect(img,(cx-w//2,cy-h//2,w,h),20,rt=0)

    imgNew = np.zeros_like(img,np.uint8)
    for rect in rectList:        
        cx,cy = rect.posCenter
        w,h = rect.size
        cv2.rectangle(imgNew,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),rect.colorR,cv2.FILLED)
        cvzone.cornerRect(imgNew,(cx-w//2,cy-h//2,w,h),20,rt=0)
    out = img.copy()
    alpha = 0.1
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]

    cv2.imshow("Image",out)
    cv2.waitKey(1)