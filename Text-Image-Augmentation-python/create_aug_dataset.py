import os

import cv2
from augment import distort, stretch, perspective
import sys
import glob

if __name__ == '__main__':
    image_path = sys.argv[1]
    augment_method = sys.argv[2]
    augment_path = image_path + '_' + augment_method
    os.makedirs(augment_path,exist_ok=True)

    images = os.listdir(image_path)

    if augment_method == 'distort':
        aug_func = distort
    if augment_method == 'stretch':
        aug_func = stretch
    if augment_method == 'perspective':
        aug_func = perspective

    for im in images:
        try:
            img = cv2.imread(os.path.join(image_path, im))
            distort_img = aug_func(img, 4)
            cv2.imwrite(os.path.join(augment_path, im), distort_img)
        except:
            print(1)
