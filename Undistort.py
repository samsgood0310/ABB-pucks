import cv2
import yaml
import numpy as np

with open("calibration_matrix.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

print(data)

mtx = data['camera_matrix']
dist = data['dist_coeff']

mtx = np.asarray(mtx, dtype=np.float32)
dist = np.asarray(dist, dtype=np.float32)

img = cv2.imread('bilde_47.png')

dst = cv2.undistort(img, mtx, dist, None, mtx)

cv2.imwrite('test_result4.png', dst)

