import numpy as np
import os
#import cv2
IMG_SIZE = 200



def getDirName(text):
    return text.split(" ")[0].title()


# def to_gray_scale(image_path):
#     img_array = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     new_image_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
#     cv2.imwrite(image_path, img=new_image_array)
#     pass
