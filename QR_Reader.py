import cv2
from pyzbar.pyzbar import decode
import numpy as np
import config


def QR_Scanner(img, thresh_incr=0):
    """Scan QR codes from image. Returns position, orientation and image with marked QR codes"""

    blur = cv2.bilateralFilter(src=img, d=9, sigmaColor=75, sigmaSpace=75)
    grayscale = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)  # Make grayscale image for filtering and thresholding
    # Thresholding for greater contrast:
    ret, threshBlur = cv2.threshold(grayscale, 50 + thresh_incr, 255, cv2.THRESH_BINARY)

    data = decode(threshBlur)  # Reading the QR-codes and their positions
    sorted_data = sorted(data, key=lambda x: x[0])  # Sort the QR codes in ascending order

    for QR_Code in sorted_data:  # Go through all QR codes
        polygon = np.int32([QR_Code.polygon])  # Convert from int64 to int32, polylines only accepts int32
        cv2.polylines(img, polygon, True, color=(0, 0, 255), thickness=10)  # Draw lines around QR-codes

        points = polygon[0]  # Extract corner points
        x1 = points[0][0]
        y1 = points[0][1]
        x2 = points[3][0]
        y2 = points[3][1]

        angle = np.rad2deg(np.arctan2(-(y2 - y1), x2 - x1))  # Calculate the orientation of each QR code
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        position = (sum(x) / len(points), sum(y) / len(points))  # Calculate center of each QR code

        # Draw circles in the middle of QR codes:
        cv2.circle(img, center=(int(position[0]), int(position[1])), radius=10, color=(255, 0, 0), thickness=-1)

        width, height, channels = img.shape
        # TODO: !!! CHANGE "position" TO LIST, MAKES FOR EASIER TRANSFORMATIONS OF COORDINATES !!!
        position = (position[0] - width/2, position[1] - height/2)  # Make center of image (0,0)

        puck = str(QR_Code.data, "utf-8")  # The data in the QR codes matches the keywords in the puck dictionary
        # Update Fill in the lists of position, orientation and number of pucks detected:

        if puck not in config.puckdict:
            config.puckdict[puck] = {"position": position, "angle": angle}

        # TODO: Make center of image (0,0) and give the resulting position list in the right form.
        #  np.array might not have the same form as the coordinates in the work space.
        #  This must be corrected for before giving positions to RAPID.

    return img


img = cv2.imread("QRKodeBord.jpg")
img = QR_Scanner(img, 130)
#print(config.puckdict)
#print(config.puckdict.items())
for key, value in config.puckdict.items():
    print(key, value)
