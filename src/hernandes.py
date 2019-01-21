


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