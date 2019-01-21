import cv2 
import numpy as np
import matplotlib.pyplot as plt
import mahotas
from centroid import getCentroid 


def regionOfInterst(image):
    height = image.shape[0]
    polygons = np.array([
        [(200,height),(1100,height),(550,250)]
    ])
    mask = np.zeros_like(image)
    print (mask)
    print (polygons)
    cv2.fillPoly(mask,polygons,255)
    maskedImage = cv2.bitwise_and(image,mask)
    return maskedImage
    
def escreve(img, texto, cor=(255,0,0)):
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, texto, (10,20), fonte, 0.5, cor, 0, cv2.LINE_AA)


image = cv2.imread("test_image5.jpg") #ler a imagem
laneImage= np.copy(image)
cv2.imshow('result',image)
cv2.waitKey(0) 
gray = cv2.cvtColor(laneImage, cv2.COLOR_RGB2GRAY)
cv2.imshow('result',gray)
cv2.waitKey(0) 
blur = cv2.GaussianBlur(gray,(5,5),0)
cv2.imshow('blur',blur)
gaus = cv2.adaptiveThreshold(blur, 125, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 91, 15)
cv2.imshow('gaus',gaus)
cv2.waitKey(0) 


T = mahotas.thresholding.otsu(blur)
bin = blur.copy()
bin[bin > T] = 255
bin[bin < 255] = 0
bin = cv2.bitwise_not(bin)

cv2.waitKey(0) 
canny = cv2.Canny(bin,50,150)
cv2.imshow('canny',canny)
cv2.waitKey(0) 
maskedImage = cv2.bitwise_and(gaus,canny)
cv2.imshow('maskedImage',maskedImage)
cv2.waitKey(0) 





(lx, objetos, lx) = cv2.findContours(maskedImage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#objetos  contem um vetor de vetor de pontos para formar o contorno
imgC2 = image.copy()
for i in objetos:
    
    cv2.circle(imgC2, getCentroid(i), 5, (0, 255, 0),5)



cv2.imshow("Imagem Original", image)
cv2.drawContours(imgC2, objetos, -1, (255, 0, 0), 2)
escreve(imgC2, str(len(objetos))+" objetos encontrados!")
cv2.imshow("Resultado", imgC2)

cv2.waitKey(0)


