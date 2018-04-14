import numpy as np
import cv2
import math

def roi(frame,vertice):
    mask=np.zeros_like(frame)
    cv2.fillPoly(mask,vertice,255)
    masked=cv2.bitwise_and(frame,mask)
    return masked
#cap=cv2.VideoCapture(0)

#Process for lines on the road 
def slope(vx1, vx2, vy1, vy2):         #Parameters to calculate slope 
     m=float(vy2-vy1)/float(vx2-vx1)        #Slope equation 
     theta1 = math.atan(m)                  #calculate the slope angle 
     return theta1*(180/np.pi)              #Calculated angle in radians 
     
cap=cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,320)
while True: 
     ret,frame = cap.read()  

     hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
     low_white=np.array([0,0,150],dtype=np.uint8)
     high_white=np.array([255,255,255],dtype=np.uint8)
     mask=cv2.inRange(hsv,low_white,high_white)
 
 #frame = cv2.resize(frame1,(600,600))           #resize video source 
     height,width=frame.shape[:2]
     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #converted to gray 
     edges=cv2.Canny(gray,70,210)
     blur=cv2.blur(edges,(5,5))
# equ = cv2.equalizeHist(gray)          #Using histogram equalization function 
     vertice=np.array([[(50,height),(width/2-45,height/2+60),(width/2+45,height/2+60),(width-50,height)]],dtype=np.int32)
     ROI_img=roi(blur,[vertice])

    # video = cv2.cvtColor(,cv2.COLOR_GRAY2BGR) 
    # cv2.rectangle(video, (roiX, roiY), (w,h), (255, 0, 0),1)  
    
     #Length for lines to find 
     #lines = cv2.HoughLinesP(mask,1,np.pi/180,10,minLineLength,maxLineGap) 150,40
     lines=cv2.HoughLinesP(ROI_img,1,1*np.pi/180,10,10,40)
     frameClone = frame.copy() 
     if lines is not None:
         for line in lines:
             x1,y1,x2,y2=line[0]

    # for x1,y1,x2,y2 in lines[0]: 
             if (round(x2-x1)!=0): 
                arctan = slope(x1,x2,y1,y2) 
                if (round(arctan>=round(-80)) and round(arctan<=round(-30))): 
            #cv2.line(frameClone,(x1+50,y1 +110),(x2+50,y2 +110),(0,255,0),2) 
                    cv2.line(frameClone,(x1,y1),(x2,y2),(0,255,0),2)
                if ( round(arctan>=round(30)) and round(arctan<=round(80))): 
                    cv2.line(frameClone,(x1,y1 ),(x2 ,y2),(0,255,0),2) 
     #cv2.imshow('frame',mask) 
     cv2.imshow('white',mask)
     cv2.imshow('ROI',ROI_img)
     cv2.imshow('DETECTING LINES',frameClone) 
     if cv2.waitKey(1) & 0xFF == ord('q'): 
         break 
cap.release() 
cv2.destroyAllWindows() 

