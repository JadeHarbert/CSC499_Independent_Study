import cv2
import os
import pytesseract

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
# inputImgName = r'\Complicated2.jpg'
inputImgName = r'/Goldfish.jpg'
inputImgDir = inputDirectory + inputImgName


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
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))

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
for cnt in contours:
    i += 1
    percentComplete = '%.2f' % (i/len(contours) * 100)
    print(str(percentComplete) + "%")
    # print("Drawing Rectangle: " + str(i))
    # print("Drawing Rectangle")
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
rectImg = outImgDirectory + r"\Rectangles.jpg"
cv2.imwrite(rectImg, im2)
