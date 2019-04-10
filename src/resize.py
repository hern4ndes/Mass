import os, os.path
import cv2

quant_imagens = len([name for name in os.listdir('.') if os.path.isfile(name)]) 

prefix_name = 'trash'
type_file = ".jpg"
new_width = 720

for i in range(1,quant_imagens):
    
    file_name = prefix_name + str(i) + type_file
    print(file_name)

    oriimg = cv2.imread(file_name)
    height, width, depth = oriimg.shape
    imgScale = new_width/width


    print("Altura = {}, Largura = {}".format(height,width))

    newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
    print("Altura nova = {}, Largura nova  = {}".format(newY,newX))
    newimg = cv2.resize(oriimg,(int(newX),int(newY)))
    cv2.imwrite("resizeimg"+ str(i)+".jpg",newimg)

    