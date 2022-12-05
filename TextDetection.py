"""
Utilizes OpenCV and OCR to detect text from an image
Author: Jade Harbert
"""
from pathlib import Path
import cv2
import pytesseract
from Regex import get_dictionary


def detect_text(input_file_path, method):
    """
    Detects the contours from the image at input_file_path and does OCR on the image to produce text
    :param method: int
        Represents which method of text detection to use
    :param input_file_path: pathlib.WindowsPath
        Path to the input file
    :return: dict
        Items along with their amounts and percentages
    """

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    outImgDirectory = Path.cwd().joinpath('Output Images')
    outFilesDirectory = Path.cwd().joinpath('Output Files')

    inputImgDir = input_file_path
    img = cv2.imread(inputImgDir)
    # Converts the frame from color to grey

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    greyImgName = "Grey Image.jpg"
    greyImgDir = outImgDirectory.joinpath(greyImgName)
    cv2.imwrite(greyImgDir.__str__(), grey)

    # Perform OTSU threshold
    ret, thresh1 = cv2.threshold(grey, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Saving threshold image
    threshImgName = 'Threshold Image.jpg'
    threshImg = outImgDirectory.joinpath(threshImgName)
    cv2.imwrite(threshImg.__str__(), thresh1)

    # Specifying structure shape and kernel size
    # increases or decreases the area of the rectangle to be detected
    # A smaller value like (10, 10) will detect each word instead of a sentence
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Saving dilation image
    dilationImgName = "Dilation Image.jpg"
    dilationImg = outImgDirectory.joinpath(dilationImgName)
    cv2.imwrite(dilationImg.__str__(), dilation)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Creating a file for recognized words
    recognizedTxtName = "Recognized Words.txt"
    recognizedTxtFile = outFilesDirectory.joinpath(recognizedTxtName)

    if method == 1:
        im2 = img.copy()
        file = open(recognizedTxtFile, "w+")
        file.write("")
        file.close()

        # Loops through the identified contours
        # Then rectangular part is cropped and passed on to
        # pytesseract for extracting text from it
        # Extracted text is then written into the text file
        print('Performing method 1, this may take a minute')
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # Drawing a rectangle on the image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]
            file = open(recognizedTxtFile, "a")
            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)
            file.write(text)
            file.write("\n")
            file.close()

        rectImgName = 'Rectangles.jpg'
        rectImg = outImgDirectory.joinpath(rectImgName)
        cv2.imwrite(rectImg.__str__(), im2)
    if method == 2:
        # Second OCR Method:
        im3 = img.copy()
        file = open(recognizedTxtFile, "w+")
        file.write("")
        file.close()

        print("Performing method 2, this may take a minute")

        all_areas = []
        # Loops through all the contours to add the contours that produce a 4-sided polygon to a list
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                all_areas.append(cv2.contourArea(cnt))

        # Sorts through the 4-sided polygons to find the largest polygon with the largest area
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        largest_item = sorted_contours[0]

        # Draws the largest 4-sided polygon
        cv2.drawContours(im3, largest_item, -1, (0, 255, 0), 3)

        # Gets the bounds of the largest 4-sided polygon and crops the image
        x, y, w, h = cv2.boundingRect(largest_item)
        cropped = im3[y:y + h, x:x + w]

        file = open(recognizedTxtFile, "a")

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

        # Writes the result of OCR to a file
        file.write(text)
        file.close()

        # Saves the image with the rectangle drawn on it
        rectImgName = "Rectangles.jpg"
        rectImg = outImgDirectory.joinpath(rectImgName)
        cv2.imwrite(rectImg.__str__(), im3)

    # Converts the output of OCR to dictionary values that have {name of nutrition item : (amount, percentage)}
    nutrition = get_dictionary(recognizedTxtFile)
    return nutrition
