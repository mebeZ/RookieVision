from Shapes import ShapeDetector
import argparse
import imutils
import numpy as np
import cv2
import time
import random

cap = cv2.VideoCapture(0)

while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([31, 90, 60])
    upper_blue = np.array([35, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)


    cv2.imshow('frame',frame)

    resized = imutils.resize(mask, width=300)
    ratio =  mask.shape[0] / float(resized.shape[0])

    cnts = cv2.findContours(mask.copy(), cv2.RETR_CCOMP,
                            cv2.CHAIN_APPROX_TC89_L1)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    sd = ShapeDetector()
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        try:
            M = cv2.moments(c)
            if(M["m00"] == 0):
                M["m00"] = 1
            cX = int((M["m10"] / M["m00"]) * 1)
            cY = int((M["m01"] / M["m00"]) * 1)
            cPerimeter = cv2.arcLength(c, True)
            shape = sd.detect(c)
            # multiply the contour (x, y)-coordinates by the resize ratio,
           # then draw the contours and the name of the shape on the image

            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            if( cPerimeter > 50):
                cv2.drawContours(mask, [c], -1, (0, 255, 0), 2)
                cv2.putText(mask, shape, (cX, cY + 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2, cv2.LINE_AA)
        except ZeroDivisionError:
            pass

        # show the output image
    cv2.imshow('mask', mask)
    cv2.imshow("Image", mask)


    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):
        break



cv2.destroyAllWindows()
cap.release()