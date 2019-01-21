import cv2 
import numpy as np
import matplotlib.pyplot as plt

def regionOfInterst(image):
    height = image.shape[0]
    polygons = np.array([
        [(200,height),(1100,height),(550,250)]
    ])
    mask = np.zeros_like(image)
    print (mask)
    print (polygons)
    #cv2.fillPoly(mask,polygons,255)
    maskedImage = cv2.bitwise_and(image,mask)
    return maskedImage


image = cv2.imread('test_image2.jpg')
laneImage= np.copy(image)
cv2.imshow('result',image)
cv2.waitKey(0) 
gray = cv2.cvtColor(laneImage, cv2.COLOR_RGB2GRAY)
cv2.imshow('result',gray)
cv2.waitKey(0) 
blur = cv2.GaussianBlur(gray,(5,5),0)
cv2.imshow('result',blur)
cv2.waitKey(0) 
canny = cv2.Canny(blur,50,150)
cv2.imshow('result',regionOfInterst(canny))
cv2.waitKey(0) 