import copy
import cv2
import numpy as np
import math
import time
import keyboard
from pythontuio import TuioServer
from pythontuio import Cursor

###########
# globals #
###########

THRESHOLD = 10

BLUR1 = 15  # 15
BLUR2 = 7  # 7

AREA_CONTURE = 3
FINGER_THRESHOLD = 25

FRAME_START = 0  # 500
SPEED = 50
###################
# ProcessTracking #
###################


class ProcessTracking:

    def __init__(self, cap):
        self.cap = cap
        self.counter = 0
        self.currentFingers = []
        self.oldFingers = []
        self.server = TuioServer("127.0.0.1", 3333)
        self.max_x = 0
        self.max_y = 0
        pass

    def addCursor(self, finger):
        x = finger[1]
        y = finger[2]
        normalized_x = x / self.max_x
        normalized_y = y / self.max_y
        cursor = Cursor(finger[0])
        cursor.position = (normalized_x, normalized_y)
        self.server.cursors.append(cursor)
        # print(cursor.position, ",")

    def processVideo(self):
        firstFrame = True
        if (cap.isOpened() == False):
            print("Error opening video stream or file")
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                if (firstFrame):
                    diffbase = frame.copy()
                    cap.set(cv2.CAP_PROP_POS_FRAMES, FRAME_START)
                    self.max_x = diffbase.shape[1]
                    self.max_y = diffbase.shape[0]
                    firstFrame = False
                result = self.processFrame(frame, diffbase)

                scale_percent = 50  # percent of original size
                width = int(frame.shape[1] * scale_percent / 100)
                height = int(frame.shape[0] * scale_percent / 100)
                dim = (width, height)

                cv2.imshow('Processed', cv2.resize(
                    result, dim, interpolation=cv2.INTER_AREA))
                # cv2.moveWindow('Processed', 0,600)
                cv2.imshow('Gray', cv2.resize(
                    self.gray, dim, interpolation=cv2.INTER_AREA))
                # cv2.moveWindow('Gray', 0,-100)
                cv2.imshow('Original', cv2.resize(
                    frame, dim, interpolation=cv2.INTER_AREA))
                # cv2.moveWindow('Original', 450,0)
                # while keyboard.is_pressed('w'):
                #    pass

                # Press Q on keyboard to  exit
                if cv2.waitKey(SPEED) & 0xFF == ord('q'):
                    break

            else:
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def processFrame(self, currentFrame, diffbase):
        diffrence = cv2.absdiff(currentFrame, diffbase)
        blured = cv2.blur(diffrence, (BLUR1, BLUR1))

        diffrence2 = cv2.absdiff(blured, diffrence)
        blured2 = cv2.blur(diffrence2, (BLUR2, BLUR2))

        _, diffrence = cv2.threshold(
            blured2, THRESHOLD, 255, cv2.THRESH_BINARY)

        self.gray = cv2.cvtColor(diffrence, cv2.COLOR_BGR2GRAY)

        # Find contours
        contours, hierarchy = cv2.findContours(
            self.gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        drawing = np.zeros(
            (currentFrame.shape[0], currentFrame.shape[1], 3), dtype=np.uint8)

        self.currentFingers.clear()
        for contour in contours:
            self.processContour(contour)
        self.nearest_neighbor()

        self.server.cursors.clear()
        for finger in self.currentFingers:
            # Position of the text slightly above the finger
            self.addCursor(finger)
            text_position = (finger[1], finger[2] - 10)
            cv2.putText(drawing, str(
                finger[0]), text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.circle(drawing, (finger[1], finger[2]), 5, (0, 0, 255), -1)
        self.server.send_bundle()
        # print(self.currentFingers)
        return drawing

    def processContour(self, contour):
        if (cv2.contourArea(contour) > AREA_CONTURE):
            x, y, width, height = cv2.boundingRect(contour)
            center_x = x + width // 2
            center_y = y + height // 2
            self.currentFingers.append([0, center_x, center_y])

    def nearest_neighbor(self):
        for currentfingerIndex, currentfinger in enumerate(self.currentFingers):
            minDistance = math.inf
            minDistanceFinger = -1
            for oldFingerIndex, oldFinger in enumerate(self.oldFingers):
                thisDistance = math.dist(
                    (currentfinger[1], currentfinger[2]), (oldFinger[1], oldFinger[2]))
                if thisDistance < FINGER_THRESHOLD and thisDistance < minDistance and oldFinger[0] != -1:
                    minDistance = thisDistance
                    minDistanceFinger = oldFingerIndex
            if minDistanceFinger != -1:
                currentfinger[0] = self.oldFingers[minDistanceFinger][0]
                self.oldFingers[minDistanceFinger][0] = -1
            else:
                currentfinger[0] = self.getNextID()
        self.oldFingers = copy.deepcopy(self.currentFingers)

    def getNextID(self):
        self.counter = self.counter + 1
        return int(self.counter)

########
# main #
########


# cap = cv2.VideoCapture('mt_camera_raw.AVI')
cap = cv2.VideoCapture('camera_test.AVI')
fingerTracking = ProcessTracking(cap)
fingerTracking.processVideo()
