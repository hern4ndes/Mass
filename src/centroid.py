import numpy as np
def getCentroid(points = []):
    sumX = 0
    sumY = 0
    for i in points:
            
            sumX += i[0][0]
            sumY += i[0][1]

    return (int(sumX/len(points)),int(sumY/len(points)))

def getdistance(pontoA=[0,0],pontoB =[0,0]):

        difX = pontoA[0] - pontoB[0]
        difY = pontoA[1] - pontoB[1]
        return(difX**2+difY**2)**(1/2)

def getalldistance(centroids = []):
        matrixdistances = np.zeros((len(centroids),len(centroids)), dtype=np.int)
        for i in  range(len(centroids)):
                for j in range(len(centroids)):
                        # print (centroids[j])
                        if (centroids[i] != None) and (centroids[j] != None):
                                distance = 0
                                distance = getdistance(centroids[i],centroids[j])
                         
                                matrixdistances[i][j] = distance

        # aqui ja tem se a maatrix de pontos
        #começando do ponto 0 encontrar o menor caminho
        #numero de arestas = n-1, onde n é o len de centroids
        n = (len(centroids)) 
       
        indice = 0 #vairavel das linhas
        caminho = []

        for i in range(n): # variavel das colunas
                minimo = 10000 #valor aleatorio 
                dist = matrixdistances[indice][i]
               
                if(i!=indice):
                        print("dist = ", end = " ")
                        print(dist)
                        if(dist < minimo):
                                        minimo = dist
                                        indice = i
                                        caminho.append(centroids[i])
                                        
        
        
       
        return caminho
             
               
                        

       