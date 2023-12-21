import cv2
import cv2.aruco as aruco
import numpy as np
import os
def findArucoMarkers(img, draw=True):                            
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    parameters =  cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)
    bboxs, ids, rejected = detector.detectMarkers(gray)
    # print(ids)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)
    return [bboxs, ids]

def arucoAug(bbox, id, img, imgAug, drawId = True):
    tl = bbox[0][0][0], bbox[0][0][1]
    tr = bbox[0][1][0], bbox[0][1][1]
    br = bbox[0][2][0], bbox[0][2][1]
    bl = bbox[0][3][0], bbox[0][3][1]
    h, w, c = imgAug.shape
    pts1 = np.array([tl, tr, br, bl])
    pts2 = np.float32([[0,0], [w,0], [w,h], [0,h]])
    matrix, _ = cv2.findHomography(pts2, pts1)
    imgout = cv2.warpPerspective(imgAug, matrix, (img.shape[1], img.shape[0]))

    dists = [0,0,0,0,0]

    print(bbox[0])

    #aruco.estimatePoseSingleMarkers(bbox[0], 0.02, matrix, dists)

    #aruco.drawAxis(imgAug, matrix, dists)

    cv2.fillConvexPoly(img, pts1.astype(int), (0, 0, 0))
    imgout = img + imgout
    return imgout
cap = cv2.VideoCapture(0)
imgAug = cv2.imread("/data/ljk.png")
while True:
    success, img = cap.read()
    arucofound = findArucoMarkers(img)
    # loop through all the markers and augment each one
    if len(arucofound[0])!=0:
        for bbox, id in zip(arucofound[0], arucofound[1]):
            img = arucoAug(bbox, id, img, imgAug)
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()