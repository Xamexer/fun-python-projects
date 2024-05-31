import cv2 as cv
import numpy as np
from PIL import Image
from os import path

##
# @file Ball Type Module
#
# @brief Detect the Colors of the Balls by getting their tracked position and test for HSV Color Values.

# Path of the File containing the HSV Values to track the different Color
colorRangeFile = "./colorRanges"
#Path to the Example picture to test the Tracking/Getting the HSV Values.
relative_path = 'env_color_game_vgl.jpg' #cheat.jpg #env_color_game_vgl | Cheat.jpg -> improved Values painted on the picture using | env_color_game_vgl -> realistic photo without changees

#ColorRange -> Outer Array: Black, White, Blue, Yellow
#Inner Array: Low Hue, High Hue, Low Sat, High Sat, Low Value, High Value
# Coordinate values to Test For Balls at this positions
colorRange = [[0]*6 for i in range(4)]
ballListDummy = [[[803],[305],[9]],[[1440],[464],[9]], #yellow,black
                 [[1266],[725],[9]],[[980],[590],[9]], #white,blue
                 [[1310],[461],[9]],[[1440],[512],[9]]] #yellow,blue

## Radius around the coordinates to avoid Errors due to Reflecting light on the balls or slightly bad tracked coordinates.
checkingRadius = 8 # + middle

#debug variables
max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'


## @Function: Trackbars
# Define the trackbars to slide between the HSV Values and save them
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)  

## @Function debugFindColorValuesMode()
# @brief debug mode to Change the Color Range Values in the File to test for the right HSV Ranges
# defining the size of the Picture
# getting the Image Path by Joining the actual absolute path with the relative path of the image File and making it an opencv image
# Creating an Window with sliders to see the picture in different HSV Mode so the Dev can try different Ranges out to
# to Filter the Ball Colors on an Optimum
# Saving the HSV Values into the File

def debugFindColorValuesMode(): # for debugging
  # color image
    width = 700
    height = 500
    absolute_path = path.dirname(__file__)
    imgPath = path.join(absolute_path, relative_path)
    opencvImg = cv.imread(imgPath)
    cv.namedWindow(window_capture_name, cv.WINDOW_NORMAL)
    cv.namedWindow(window_detection_name, cv.WINDOW_NORMAL)
    cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
    cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
    cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
    cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
    cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
    cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)
    cv.createButton("Add to file",addToFile,None,cv.QT_PUSH_BUTTON,1)
    cv.createButton("Clear file",clearFile,None,cv.QT_PUSH_BUTTON,1)
    while True:
        if opencvImg is None:
            break
        frame_HSV = cv.cvtColor(opencvImg, cv.COLOR_RGB2HSV)
        frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
        cv.resizeWindow(window_detection_name, width, height)
        cv.resizeWindow(window_capture_name, width, height)
        cv.imshow(window_capture_name, opencvImg)
        cv.imshow(window_detection_name, frame_threshold)
        key = cv.waitKey(30)
        if key == ord('q') or key == 27:
            break
def addToFile(*args):
    print(args)
    file = open(colorRangeFile,"a")
    file.write("\n#" + str(low_H).zfill(3) + " #" + str(high_H).zfill(3) + " #" + str(low_S).zfill(3) + " #" + str(high_S).zfill(3) + " #" + str(low_V).zfill(3) + " #" + str(high_V).zfill(3))
    file.close()
def clearFile(*args):
    print(args)
    file = open(colorRangeFile,"w")
    file.write("LH   HH   LS   HS   LV   HV #Order: Black, White, Blue, Yellow")
    file.close()


## @Function: importBallColorValues
# going threw the File with the HSV Color Values and
# filling the Array with these Values
def importBallColorValues():
    with open(colorRangeFile) as file:
        next(file)
        index = 0
        for line in file:
            for i in range(0,6):
                colorRange[index][i] = int(line[i*5+1:i*5+4])
                #print(int(line[i*5+1:i*5+4]))
            index=index+1


## @Function: getBallTypes
# Converting the image from RGB to HSV
# Saving the colors of the Balls on the Specific Position/coordinates
# Test IF the Pixel on the ball Position is between the High and Low HSV Values, so in between the Range from the ColorRange File
# output some response for the Devs
# @return List of All by Color detected Balls
def getBallTypes(ballList,colorImage): #(ballList, colorImage)
    estimatedColorArray = []
    hsvFrame = cv.cvtColor(colorImage, cv.COLOR_RGB2HSV)
    for ballIndex, ball in enumerate(ballList):
        colorOfBallPixel = hsvFrame[(ball[1][0] + checkingRadius)][ball[0][0] + checkingRadius]
        indexColor = 0
        for pixelX in range(0,checkingRadius*2 + 1):
            for pixelY in range(0,checkingRadius*2 + 1):
                colorOfBallPixel = hsvFrame[ball[1][0] - checkingRadius + pixelY,ball[0][0] - checkingRadius + pixelX]
                for color in colorRange:
                    if(int(colorOfBallPixel[0]) >= int(color[0]) and int(colorOfBallPixel[0]) <= int(color[1]) and #check if Ball Hue is in Hue Range
                       int(colorOfBallPixel[1]) >= int(color[2]) and int(colorOfBallPixel[1]) <= int(color[3]) and #check if Ball Sat is in Sat Range
                       int(colorOfBallPixel[2]) >= int(color[4]) and int(colorOfBallPixel[2]) <= int(color[5])): #check if Ball Value is in Value Range
                        estimatedColorArray.append(indexColor)
                        break
                    indexColor=indexColor+1
                indexColor = 0
        if not estimatedColorArray:
            print("------No clue what color this ball got")
        else:
            mostFrequentColor = most_frequent(estimatedColorArray)
            print("-----Ball color is " + getColorCode(mostFrequentColor))
            ball[2] = mostFrequentColor
        estimatedColorArray.clear()
    return ballList #ColorCode; 0 = Black , 1 = White, 2 = Blue, 3 = Yellow, 9 = Undefined
def getColorCode(dummy):
    if dummy == 0:
        return "Black"
    elif dummy == 1:
        return "White"
    elif dummy == 2:
        return "Blue"
    elif dummy == 3:
        return "Yellow"
    else:
        return "No fucking clue"

def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
    return num

## @function: main
# putting the Color Values from the File into the Array (colorRangesFile -> colorRange)
# getting the absolute Path From ? and adding the Path together with the relative Path (contaning the Folder and Image with the Example Pictures.
# putting the image from the path into an Image Variable
# Testing for the Color by comparing the color at the colorImage on the position from the ballListDummy
def main():
    importBallColorValues()
    absolute_path = path.dirname(__file__) ## --- IDK
    imgPath = path.join(absolute_path, relative_path)
    colorImage = cv.imread(imgPath)
    getBallTypes(ballListDummy,colorImage)


## @MAIN
# Starting the main Function, OR, incase main() is outcommented and "debugFindColorValuesMode() not outcommented you can start the program in debugmode to change the searched HSV Values
main() #Starting module
#debugFindColorValuesMode() #Starting in Debug mode