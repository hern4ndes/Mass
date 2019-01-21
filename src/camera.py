import cv2 
import numpy as np
import matplotlib.pyplot as plt
import mahotas
from centroid import * 

cap = cv2.VideoCapture(0)

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
    cv2.putText(img, texto, (10,20), fonte, 0.5, cor, 0,
    cv2.LINE_AA)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
   
    blur = cv2.GaussianBlur(gray,(9,9),0)
    #blur = cv2.bilateralFilter(gray, 11, 77, 77)
    blur = cv2.medianBlur(gray, 15)
    T = mahotas.thresholding.otsu(blur)
    bin = blur.copy()
    bin[bin > T] = 255
    bin[bin < 255] = 0
    bin = cv2.bitwise_not(bin)

    
    canny = cv2.Canny(bin,50,150)

    lx,objetos,lx = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #print(objetos)
    imgC2 = canny.copy()
    centroids = []
    for i in objetos:
        #print(getCentroid(i))
        centroid = getCentroid(i)
        cv2.circle(imgC2, centroid, 5, (0, 255, 0),2)
        centroids.append(centroid)
    path = getalldistance(centroids)
    
    for i in range(0,len(path)-1):
       
        cv2.line(imgC2,path[i], path[i+1],(0,0,255),1,1)

    
  


    #cv2.imshow("Imagem Original", frame)
    cv2.drawContours(imgC2, objetos, -1, (255, 0, 0), 2)
    escreve(imgC2, str(len(objetos))+" objetos encontrados!")
    cv2.imshow("Resultado", imgC2)
    

    
    #cv2.imshow('frame',blur)q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()