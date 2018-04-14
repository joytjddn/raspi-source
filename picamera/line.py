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
     cap.set(3,320)
     cap.set(4,320)

     while True:
         ret, frame = cap.read()
         height,width=frame.shape[:2]
         gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
         blur=cv2.blur(gray,(5,5))
         edges=cv2.Canny(blur,70,210)
         
         vertices = np.array([[(50,height),(width/2-45, height/2+60), (width/2+45, height/2+60), (width-50,height)]], dtype=np.int32)
         mask=np.zeros_like(edges)
        
        #cv2.fillPoly(mask,vertices,color=255)
         ROI_img = cv2.bitwise_and(edges,mask)
        # line = cv2.HoughLinesP(edges, 1, np.pi/180, minLineLength, maxLineGap)
         line=cv2.HoughLinesP(ROI_img,1,1*np.pi/180,30,10,20)
#drawline
         drawline=cv2.line(frame,line,color=[0,0,255],2)
         cv2.imshow('Origin', frame)
         cv2.imshow('gray',gray)
         cv2.imshow('edges',edges)
#        cv2.imshow('Green',G)
         if cv2.waitKey(1)&0xFF==ord('q'):
              break;
     cv2.destroyAllwindows()
track()
