import cv2
import pytesseract
from pytesseract.pytesseract import image_to_string as imtstr
import numpy as np
import sys
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'




img = cv2.imread('FindMind_image1.jpg')
img2 = cv2.imread('FindMind_image2.jpg')
img3 = cv2.imread('FindMind_image3.jpg')

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)

    kernel = np.ones((2, 1), np.uint8)
    img = cv2.erode(gray, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    return img


# ### Format of DOB
# 2 numbers / 2 numbers / 4 numbers (10 characters)

def dob(list):
    for dob in list:
        if len(dob) == 10 and dob[0:1].isnumeric() and dob[3:4].isnumeric and dob[6:9].isnumeric():
            return dob

# ### Format of Pan Number
# 6 letters followed by 4 numbers and then 1 letter

def pan_identifier(first_list):
    for pan in first_list:
        if len(pan) == 10 and pan[0:5].isalpha() and pan[6:9].isnumeric():
            pan[0:5].upper()
            return (pan)


def CV_task(img):
    img = preprocess(img)
    first_list = imtstr(img, nice=0, output_type='string', timeout=0).split()
    if dob(first_list) == None:
        img = cv2.transpose(img)
        img = cv2.flip(img,flipCode=1)
        x = 260
        y= 450
        h = 100
        w = 180
        img2 = img[y:y+h, x:x+w].copy()
        #plt.imshow(img2)
        first_list = imtstr(img, nice=0, output_type='string', timeout=0).split()
        sec_list = imtstr(img2, nice=0, output_type='string', timeout=0).split()
        #print(sec_list)
        print(pan_identifier(first_list))
        print(dob(sec_list))
    else:
        print(pan_identifier(first_list))
        print(dob(first_list))

sys.stdout = open("output_CVTask.txt", "w")

CV_task(img)
CV_task(img2)
CV_task(img3)

sys.stdout.close()