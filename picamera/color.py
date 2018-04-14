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
     cap.set(3,480)
     cap.set(4,320)
     while True:
         ret, frame = cap.read()
 #element
         element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 #color range
         lower_red = np.array([-10,100,100])#[-10,50,80][100,255,255]
         upper_red = np.array([10,255,255])
         lower_green = np.array([30,100,100])#[30,30,70][50,255,255]
         upper_green = np.array([50,255,255])
 #green
         mask_green = cv2.inRange(hsv, lower_green, upper_green)
         eroded_green = cv2.erode(mask_green, element)
         traffic_green = cv2.dilate(eroded_green, element)
         intRows,intColums=traffic_green.shape
 #draw circle
         green_circles =cv2.HoughCircles(traffic_green, cv2.HOUGH_GRADIENT,1    ,100,param1=60,param2=12,minRadius=6,maxRadius=50)
         if green_circles is not None:
            a,b,c =green_circles.shape
            for i in range(b):
                cv2.circle(frame,(green_circles[0][i][0],green_circles[0][i]    [1]), green_circles[0][i][2], (0, 0, 255), 3, cv2.LINE_AA)
 #red
         mask_red = cv2.inRange(hsv, lower_red, upper_red)
         eroded_red = cv2.erode(mask_red, element)
         traffic_red = cv2.dilate(eroded_red,element)
         intRows, intColumns = traffic_red.shape
         red_circles =cv2.HoughCircles(traffic_red, cv2.HOUGH_GRADIENT,1,100,    param1=60,param2=12,minRadius=6,maxRadius=50)
         if red_circles is not None:
             a,b,c =red_circles.shape
             for i in range(b):
                 cv2.circle(frame,(red_circles[0][i][0],red_circles[0][i][1    ]),red_circles[0][i][2], (0, 0, 255), 3, cv2.LINE_AA)
         G=cv2.bitwise_and(frame,frame,mask=mask_green)
         R=cv2.bitwise_and(frame,frame,mask=mask_red)

         cv2.imshow('Origin', frame)
 #        cv2.imshow('Green',G)
         if cv2.waitKey(1)&0xFF==ord('q'):
              break;
     cv2.destroyAllwindows()
track()
