import math
import cv2


cap = cv2.VideoCapture(1)
px_width = 1280
px_height = 960
cap.set(3, px_width)
cap.set(4, px_height)

puckdict = {}

if __name__ == "__main__":
    from matplotlib import pyplot as plt
    import numpy as np

    if "hei" not in puckdict:
        puckdict["puck3"] = {"position": [10, 20], "angle": 5}
        puckdict["puck2"] = {"position": [30, 50], "angle": 50}
        puckdict["puck2"] = {"position": [40, 60], "angle": 90}
        puckdict["puck7"] = {"position": [25, 30], "angle": -40}
        puckdict["puck4"] = {"position": [23, 10], "angle": 31}

print(puckdict)

"""ret, frame = cap.read()
if ret:
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayscale2 = grayscale.copy()
    #normalized = cv2.normalize(grayscale, None)
    #hist = cv2.calcHist([img], [0], None, [256], [0, 256])

    #cv2.normalize(grayscale2, grayscale2, alpha=0, beta=255, norm_type=cv2.NORM_L1)
    #plt.hist(grayscale2.ravel(), 256, [0, 256]);
    #plt.show()
#hstack = np.hstack((grayscale, grayscale2))
#cv2.imshow("hei", hstack)
#cv2.waitKey(0)
x, y, w, h = 364, 633, 791, 273
ROI = grayscale[y:y + h, x:x + w]

# Calculate mean and STD
mean, STD = cv2.meanStdDev(ROI)

# Clip frame to lower and upper STD
offset = 0.2
clipped = np.clip(grayscale, mean - offset * STD, mean + offset * STD).astype(np.uint8)
blur = cv2.bilateralFilter(src=grayscale, d=3, sigmaColor=75, sigmaSpace=75)
# Normalize to range
result = cv2.normalize(blur, blur, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=-1)
result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

cv2.imshow('image', grayscale)
cv2.imshow('result', result)
cv2.waitKey()"""
