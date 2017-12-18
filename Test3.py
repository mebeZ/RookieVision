from Tkinter import *
import cv2
import sys
import numpy as np

LOWER_HSV = np.array([175, 175, 175], dtype="uint8")
UPPER_HSV = np.array([255, 255, 255], dtype="uint8")

for x in range(5):
    stream = cv2.VideoCapture(x)
    stream.set(10, 0)
    stream.set(3, 320)
    stream.set(4, 240)

    if (stream.isOpened()):
        print("Camera found on port: %d" % (x))
        break;

if (not stream.isOpened()):
    print("Camera not found")
    sys.exit()

masterPanel = Tk()
lowerHLabel = Label(masterPanel, text="Lower H").grid(row=1, column=0)
lowerHScale = Scale(masterPanel, from_=0, to=180, orient=HORIZONTAL)
lowerHScale.set(LOWER_HSV[0])
lowerHScale.grid(row=1, column=1)

lowerSLabel = Label(masterPanel, text="Lower S").grid(row=2, column=0)
lowerSScale = Scale(masterPanel, from_=0, to=255, orient=HORIZONTAL)
lowerSScale.set(LOWER_HSV[1])
lowerSScale.grid(row=2, column=1)

lowerVLabel = Label(masterPanel, text="Lower V").grid(row=3, column=0)
lowerVScale = Scale(masterPanel, from_=0, to=255, orient=HORIZONTAL)
lowerVScale.set(LOWER_HSV[2])
lowerVScale.grid(row=3, column=1)

############

upperHLabel = Label(masterPanel, text="Upper H").grid(row=4, column=0)
upperHScale = Scale(masterPanel, from_=0, to=180, orient=HORIZONTAL)
upperHScale.set(UPPER_HSV[0])
upperHScale.grid(row=4, column=1)

upperSLabel = Label(masterPanel, text="Upper S").grid(row=5, column=0)
upperSScale = Scale(masterPanel, from_=0, to=255, orient=HORIZONTAL)
upperSScale.set(UPPER_HSV[1])
upperSScale.grid(row=5, column=1)

upperVLabel = Label(masterPanel, text="Upper V").grid(row=6, column=0)
upperVScale = Scale(masterPanel, from_=0, to=255, orient=HORIZONTAL)
upperVScale.set(UPPER_HSV[2])
upperVScale.grid(row=6, column=1)

while True:
    masterPanel.update()
    masterPanel.update_idletasks()

    LOWER_HSV = np.array([lowerHScale.get(), lowerSScale.get(), lowerVScale.get()], dtype="uint8")
    UPPER_HSV = np.array([upperHScale.get(), upperSScale.get(), upperVScale.get()], dtype="uint8")

    rc, source = stream.read()

    hsv = cv2.cvtColor(source, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_HSV, UPPER_HSV)
    cv2.imshow("Mask", mask)

    retval, threshold = cv2.threshold(mask, 255, 255, 255)
    cv2.imshow("Threshold", threshold)

    cv2.imshow("Stream", source)

    keyPressed = cv2.waitKey(33)

    # Space bar
    if keyPressed == 32:
        cv2.destroyAllWindows()
        sys.exit()
    elif keyPressed == ord("s"):
        cv2.imwrite("Test.jpg", source)