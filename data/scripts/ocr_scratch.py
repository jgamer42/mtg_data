import cv2 as cv
import numpy as np
def rescale(frame,scale=0.25):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dims = (width,height)
    return cv.resize(frame,dims,interpolation=cv.INTER_AREA)

def gray_scale(img):
    return cv.cvtColor(img,cv.COLOR_BGR2GRAY)

def blur(img):
    return cv.GaussianBlur(img,(7,7),cv.BORDER_DEFAULT)

def edges(img):
    return cv.Canny(img,125,175)

img = cv.imread("prueba_3.jpeg")
original = rescale(img)
img = gray_scale(original)
img = blur(img)
ret,thresh = cv.threshold(img,100,255,cv.THRESH_BINARY)

#img = edges(img)
#img = cv.dilate(img,(3,3),iterations=15)
contours, hierarchies = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE) 
print(len(contours))

blank = np.zeros(img.shape,dtype="uint8")
cv.drawContours(blank,contours,-1,(255,0,255),2)
cv.imshow("preposs", thresh)
cv.imshow("countours",blank)
cv.imshow("orignal",original)
cv.waitKey(0)


    