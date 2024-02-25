import numpy as np
import os, cv2

def horizontalFlip(img):
    size = img.shape
    h,w = size[0],size[1]
    iLR = img.copy()
    
    for i in range(h):
        for j in range(w):
            iLR[i,j] = img[i,w-j-1]
 
    return iLR

pth = list(os.walk("."))
for i in pth[0][-1]:
    img = cv2.imread("./" + i)
    img = horizontalFlip(img)
    cv2.imwrite("11" + i, img)