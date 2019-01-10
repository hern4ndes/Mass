def getCentroid(points = []):
    sumX = 0
    sumY = 0
    for i in points:
            
            sumX += i[0][0]
            sumY += i[0][1]

    return (int(sumX/len(points)),int(sumY/len(points)))