from flask import jsonify
import cv2
import PIL as pil
import numpy as np
import pytesseract
from PIL import Image
import math
import subprocess

def get_dominant_color(pil_img):
    img = pil_img.copy()
    img.convert("RGB")
    img = img.resize((1, 1), resample=0)
    dominant_color = img.getpixel((0, 0))
    return dominant_color

#from https://github.com/opencv/opencv/blob/master/samples/dnn/text_detection.py
def decodeBoundingBoxes(scores, geometry, scoreThresh):
    detections = []
    confidences = []

    ############ CHECK DIMENSIONS AND SHAPES OF geometry AND scores ############
    assert len(scores.shape) == 4, "Incorrect dimensions of scores"
    assert len(geometry.shape) == 4, "Incorrect dimensions of geometry"
    assert scores.shape[0] == 1, "Invalid dimensions of scores"
    assert geometry.shape[0] == 1, "Invalid dimensions of geometry"
    assert scores.shape[1] == 1, "Invalid dimensions of scores"
    assert geometry.shape[1] == 5, "Invalid dimensions of geometry"
    assert scores.shape[2] == geometry.shape[2], "Invalid dimensions of scores and geometry"
    assert scores.shape[3] == geometry.shape[3], "Invalid dimensions of scores and geometry"
    height = scores.shape[2]
    width = scores.shape[3]
    for y in range(0, height):

        # Extract data from scores
        scoresData = scores[0][0][y]
        x0_data = geometry[0][0][y]
        x1_data = geometry[0][1][y]
        x2_data = geometry[0][2][y]
        x3_data = geometry[0][3][y]
        anglesData = geometry[0][4][y]
        for x in range(0, width):
            score = scoresData[x]

            # If score is lower than threshold score, move to next x
            if (score < scoreThresh):
                continue

            # Calculate offset
            offsetX = x * 4.0
            offsetY = y * 4.0
            angle = anglesData[x]

            # Calculate cos and sin of angle
            cosA = math.cos(angle)
            sinA = math.sin(angle)
            h = x0_data[x] + x2_data[x]
            w = x1_data[x] + x3_data[x]

            # Calculate offset
            offset = ([offsetX + cosA * x1_data[x] + sinA * x2_data[x], offsetY - sinA * x1_data[x] + cosA * x2_data[x]])

            # Find points for rectangle
            p1 = (-sinA * h + offset[0], -cosA * h + offset[1])
            p3 = (-cosA * w + offset[0], sinA * w + offset[1])
            center = (0.5 * (p1[0] + p3[0]), 0.5 * (p1[1] + p3[1]))
            detections.append((center, (w, h), -1 * angle * 180.0 / math.pi))
            confidences.append(float(score))

    # Return detections and confidences
    return [detections, confidences]

def get_ocr_text(image_url):
    net = cv2.dnn.readNet("../model/frozen_east_text_detection.pb")
    img = cv2.imread(image_url)
    pytesseract.pytesseract.tesseract_cmd = ( r'/opt/homebrew/Cellar/tesseract/5.0.1/bin/tesseract' )

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))

    screen = cntsSorted[-2]
    x, y = [], []
    for contour in screen:
        x.append(contour[0][0])
        y.append(contour[0][1])

    x1 = min(x)
    x2 = max(x)
    y1 = min(y)
    y2 = max(y)

    cropped = None
    #EDIT THIS
    if get_dominant_color(Image.open(image_url))[0] < 127:
        cropped = cv2.bitwise_not(img[y1:y2, x1:x2])
    else:
        cropped = img[y1:y2, x1:x2]

    cropped_thresh = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
    cropped_thresh = cv2.adaptiveThreshold(cropped_thresh,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,11,2)


    inpWidth = inpHeight = 320 
    image_blob = cv2.dnn.blobFromImage(cropped, 1.0, (inpWidth, inpHeight), (123.68, 116.78, 103.94), True, False)

    output_layer = []
    output_layer.append("feature_fusion/Conv_7/Sigmoid")
    output_layer.append("feature_fusion/concat_3")

    net.setInput(image_blob)
    output = net.forward(output_layer)
    scores = output[0]
    geometry = output[1]

    confThreshold = 0.5
    nmsThreshold = 0.3
    [boxes, confidences] = decodeBoundingBoxes(scores, geometry, confThreshold)
    indices = cv2.dnn.NMSBoxesRotated(boxes, confidences, confThreshold, nmsThreshold)

    height_ = cropped.shape[0]
    width_ = cropped.shape[1]
    rW = width_ / float(inpWidth)
    rH = height_ / float(inpHeight)
    smallestX = cropped.shape[1]

    for i in indices:
        # get 4 corners of the rotated rect
        vertices = cv2.boxPoints(boxes[i])
        # scale the bounding box coordinates based on the respective ratios
        for j in range(4):
            vertices[j][0] *= rW
            vertices[j][1] *= rH
            if vertices[j][0] < smallestX and vertices[j][1] > 100:
                smallestX = vertices[j][0]

        for j in range(4):
            p1 = (int(vertices[j][0]), int(vertices[j][1]))
            p2 = (int(vertices[(j + 1) % 4][0]), int(vertices[(j + 1) % 4][1]))
            #cv2.line(cropped, p1, p2, (0, 255, 0), 3)

    code_panel = cropped[0:cropped.shape[0], int(smallestX):cropped.shape[1]]
    code_panel = cv2.cvtColor(code_panel, cv2.COLOR_RGB2GRAY)
    code_panel_thresh = cv2.adaptiveThreshold(code_panel,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,11,2)
    code_panel_thresh = cv2.resize(code_panel_thresh, (int(cropped.shape[1]*1.5), int(cropped.shape[0]*1.5)))
    cv2.imwrite("../screenshot_info/code_panel_thresh.jpeg", code_panel)
    subprocess.call(["sh", "ocr.sh"])
    with open("../screenshot_info/ocr_text.txt", 'r') as f:
        return "\n".join(f.readlines())

#get_ocr_text("./image.jpeg")