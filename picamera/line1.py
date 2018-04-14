import numpy as np
import cv2
#from PIL import ImageGrab

def draw_lines(frame,lines):
    try:
        for line in lines:
            coords=line[0]
            cv2.line(frame,(coords[0],coords[1]),(coords[2],coords[3]),[255,0,0],2)
    except:
        pass

def roi(frame,vertices):
    mask=np.zeros_like(frame)
    cv2.fillPoly(mask,vertices,255)
    masked=cv2.bitwise_and(frame,mask)
    return masked

def linetrack(frame):
    height,width=frame.shape[:2]
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    edges=cv2.Canny(gray,70,210)
    blur=cv2.blur(edges,(5,5))
    #vertices =  np.array([[10,500], [10,300], [300,200],[500,200], [800,300], [800,500]])
    vertices = np.array([[(50,height),(width/2-45, height/2+60), (width/2+45, height/2+60), (width-50,height)]], dtype=np.int32)
    ROI_img = roi(blur,[vertices])
     # line = cv2.HoughLinesP(edges, 1, np.pi/180, minLineLength, maxLineGap)
    lines=cv2.HoughLinesP(ROI_img,1,1*np.pi/180,30,10,20)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line[0]
            cv2.line(frame, (x1,y1),(x2,y2),(0,255,0),2 )

    #drawline
    draw_lines=(ROI_img,lines)
    return ROI_img

cap=cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,320)

while True:
    ret,frame=cap.read()

    # screen =np.array(ImageGrab.grab(bbox=(0,40,800,600)))
    result= linetrack(frame)

    cv2.imshow('Origin', frame)
  #  cv2.imshow('gray',gray)
   # cv2.imshow('edges',edges)
    cv2.imshow('ROI',result)
#        cv2.imshow('Green',G)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break;
cap.release()
cv2.destroyAllwindows()

