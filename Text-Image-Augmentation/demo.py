import Augment
import cv2
import numpy as np
import sys

'''
The code is for OpenCV format.
If your data format is PIL.Image, please convert the format by:

import numpy as np
import cv2
from PIL import Image

img = Image.open("The Path to the image")
img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
'''

im = cv2.imread(sys.argv[1])
# im = cv2.resize(im, (200, 64))
cv2.imshow("im_CV", im)
for i in range(5):
    im_Distort = Augment.GenerateDistort(im, 4)
    cv2.imwrite("im_Distort_{}.jpg".format(i), im_Distort)
    im_Stretch = Augment.GenerateStretch(im, 4)
    cv2.imwrite("im_Stretch_{}.jpg".format(i), im_Stretch)
    im_Perspective = Augment.GeneratePerspective(im)
    cv2.imwrite("im_Perspective_{}.jpg".format(i), im_Perspective)
