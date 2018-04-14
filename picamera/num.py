import numpy as np
import cv2

def track():
     try:
          print('ON')
          cap=cv2.VideoCapture(0)
     except:
         print('F')
         return
 #window size
     cap.set(3,240)
     cap.set(4,240)
     while True:
         ret, frame = cap.read()
         template=cv2.imread('3.jpg',0)
         w,h=template.shape[::-1]
         
         gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
         ret,thr=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
         edges=cv2.Canny(gray,170,200)
         
         circles =cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,100,param1=40,param2=50,minRadius=6,maxRadius=50)
         if circles is not None:
            circles=np.uint16(np.around(circles))
            for i in circles[0,:]:
                cv2.circle(frame,(i[0],i[1]),i[2],(255,255,0),2)
        
                res=cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED)
                loc=np.where(res>=0.8)
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(frame,pt,(pt[0]+w,pt[1]+h),(0,0,255),2)
            
 #        G=cv2.bitwise_and(frame,frame,mask=mask_green)
#         R=cv2.bitwise_and(frame,frame,mask=mask_red)

         cv2.imshow('Origin', frame)
         cv2.imshow('gray',gray)
         cv2.imshow('edges',edges)
#         cv2.imshow('Green',G)
         if cv2.waitKey(1)&0xFF==ord('q'):
             break;
     cv2.destroyAllwindows()
track()
