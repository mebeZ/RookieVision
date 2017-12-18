import cv2
import numpy as np

re = cv2.imread('ree.jpg', 1)
cv2.imshow('re', re)
print(np.uint8([re[300][10][0], re[300][10][1], re[300][10][2]]))
cv2.waitKey(0)
cv2.destroyAllWindows()