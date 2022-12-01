import os

import cv2
import pytesseract
from Nutrition import get_dictionary


def detect_text(input_file_path):
    directory = os.getcwd()
    inputDirectory = directory + r"\Input Images"
    outImgDirectory = directory + r"\Output Images"
    outFilesDirectory = directory + r"\Output Files"

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # inputImgName = r"\Example Nutrition Label 2.jpg"
    # inputImgName = r"\Cropped Example Nutrition Label 2.jpg"
    # inputImgName = r"\OPENCV Sample Image.jpg"
    # inputImgName = r"\Example Nutrition Label.png"
    # inputImgName = r"\Goldfish Nutrition Label.jpg"

    # inputImgDir = inputDirectory + inputImgName

    inputImgDir = input_file_path
    img = cv2.imread(inputImgDir)
    # Converts the frame from color to grey

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    greyImgName = r"\Grey Image.jpg"
    greyImgDir = outImgDirectory + greyImgName
    cv2.imwrite(greyImgDir, grey)

    # Perform OTSU threshold
    technique = cv2.THRESH_OTSU
    # technique = cv2.THRESH_BINARY_INV

    # ret, thresh1 = cv2.threshold(grey, 0, 255, technique)
    ret, thresh1 = cv2.threshold(grey, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    threshImg = outImgDirectory + r"\Threshold Image.jpg"
    cv2.imwrite(threshImg, thresh1)

    # Specifying structure shape and kernel size
    # increases or decreases the area of the rectangle to be detected
    # A smaller value like (10, 10) will detect each word instead of a sentence
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    dilationImg = outImgDirectory + r"\Dilation Image.jpg"
    cv2.imwrite(dilationImg, dilation)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    im2 = img.copy()

    recognizedTxtName = r"\Recognized Words.txt"
    recognizedTxtFile = outFilesDirectory + recognizedTxtName

    file = open(recognizedTxtFile, "w+")
    file.write("")
    file.close()

    # Loops through the identified contours
    # Then rectangular part is cropped and passed on to
    # pytesseract for extracting text from it
    # Extracted text is then written into the text file
    i = 0
    print("Number of Rectangles to draw: " + str(len(contours)))
    print("Drawing Rectangles:")

    all_areas = []
    for cnt in contours:
        x1, y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            # x, y, w, h = cv2.boundingRect(cnt)
            # im2 = cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
            all_areas.append(cv2.contourArea(cnt))
            # cropped = im2[y: y + h, x:x + w]

    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    largest_item = sorted_contours[0]

    cv2.drawContours(im2, largest_item, -1, (0, 255, 0), 3)

    x, y, w, h = cv2.boundingRect(largest_item)
    cropped = im2[y:y + h, x:x + w]
    file = open(recognizedTxtFile, "a")

    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped)

    file.write(text)
    file.write("\n")

    file.close()

    rectImg = outImgDirectory + r"\Rectangles.jpg"
    cv2.imwrite(rectImg, im2)

    nutrition = get_dictionary(recognizedTxtFile)
    return nutrition
