from pythontuio import TuioClient
from pythontuio import Cursor
from pythontuio import TuioListener
from threading import Thread
import cv2
import gestureRecognizerTest as gr
import copy
import numpy as np
import math
import time
import random
dim = 1024
WIREFRAME = True

# oldCursors = [[None, False, [0, 0], [0, 0]]]  # ID, TRUE, (X, Y), (X , Y)
oldCursors = []  # ID, TRUE, (X, Y), (X , Y)
cursorStartedInObject = [None]
vectors = [[None, (0, 0)]]
normalized_vectors = [[None, (0, 0)]]
translationVector = (0, 0)
wasOnScreen = False
multiplier = 1000
rectangles = [[0, [460, 400], 300, 0, (255, 100, 0), 2], [1, [380, 350], 250, 0, (100, 100, 255), 2],  [2, [650, 250], 300, 0, (50, 255, 0), 2]  # ID,CENTER, SIZE, ROTATION, COLOR, THICKNESS
              ]
circles = []
triangles = []#CENTER, SIZE, ROTATION, COLOR
selectedRect = 0


class MyListener(TuioListener):
    def update(self):
        self.rectangles = rectangles
        self.circles = circles
        self.triangles = triangles
        self.oldFingersOnScreen = []
        self.drawCursors = []
        self.lockedInFingers = 0
        self.mightClickEvent = False
        while(True):
            self.image = np.zeros((dim, dim, 3), dtype=np.uint8)
            self.drawObjects()
            for cursor in oldCursors:
                if (len(cursor) > 3):
                    for age in range(2, len(cursor)-1):
                        cv2.line(self.image, (self.normToPixel(cursor[age][0]), self.normToPixel(cursor[age][1])), (self.normToPixel(
                            cursor[age+1][0]), self.normToPixel(cursor[age+1][1])), (255, 255, 255), 2)
            for cursor in client.cursors:
                cv2.circle(self.image, (self.normToPixel(cursor.position[0]), self.normToPixel(cursor.position[1])),
                        6, (0, 0, 255), -1)
            cv2.imshow("White Blank", self.image)
            cv2.waitKey(25)
    def add_tuio_cursor(self, cursor: Cursor):
        pass

    def refresh(self, time):
        self.addOldCursors(client.cursors)
        self.calculateVectors()
        self.processMotions()
       
        return super().refresh(time)

    def drawObjects(self):
        newCircle = []
        for circle in self.circles:
            circle[1] -= 1
            if circle[1] > 1:
                newCircle.append(circle)
        self.circles = newCircle
        for circle in self.circles:
            cv2.circle(self.image, (int(circle[0][0]),int(circle[0][1])), int(circle[1]), circle[2], -1)
        
        for triangle in self.triangles:
            triangle[2] -= 2
            if triangle[2] < -360:
                triangle[2] = 0
            angle = math.radians(triangle[2])
            radius = triangle[1] / 2

            vertex1 = (int(triangle[0][0] + radius * math.cos(angle)), int(triangle[0][1] - radius * math.sin(angle)))
            vertex2 = (int(triangle[0][0] + radius * math.cos(angle + 2 * math.pi / 3)), int(triangle[0][1] - radius * math.sin(angle + 2 * math.pi / 3)))
            vertex3 = (int(triangle[0][0] + radius * math.cos(angle + 4 * math.pi / 3)), int(triangle[0][1] - radius * math.sin(angle + 4 * math.pi / 3)))

            pts = np.array([vertex1, vertex2, vertex3], np.int32)

            cv2.polylines(self.image, [pts], isClosed=True, color=triangle[3], thickness=2)
        
        for rectangle in self.rectangles:
            # Calculate the rotation matrix
            angle_radians = np.radians(rectangle[3])
            cos_theta = np.cos(angle_radians)
            sin_theta = np.sin(angle_radians)
            rotation_matrix = np.array(
                [[cos_theta, -sin_theta], [sin_theta, cos_theta]])

            # Get the four corners of the rectangle
            corners = np.array([
                [-rectangle[2] / 2, -rectangle[2] / 2],
                [rectangle[2] / 2, -rectangle[2] / 2],
                [rectangle[2] / 2, rectangle[2] / 2],
                [-rectangle[2] / 2, rectangle[2] / 2]
            ])

            # Rotate the corners
            rotated_corners = np.dot(corners, rotation_matrix.T)
            rotated_corners += (rectangle[1][0], rectangle[1][1])

            # Convert the corners to integers
            rotated_corners = np.round(rotated_corners).astype(int)

            # Draw the rotated rectangle
            if rectangle[5] == -1:
                cv2.fillPoly(self.image, [rotated_corners],
                             color=rectangle[4])
            else:
                cv2.polylines(self.image, [rotated_corners],
                              isClosed=True, color=rectangle[4], thickness=rectangle[5])
        
    def processMotions(self):
        global selectedRect

        currentFingersOnScreen = oldCursors

        print("Current fingers: ", [finger[1]
              for finger in currentFingersOnScreen])
        # click event
        if len(currentFingersOnScreen) == 0:
            scaling = 1
            if len(self.oldFingersOnScreen) == 1 and selectedRect != -1 and self.mightClickEvent:
                if self.fingerAge < 8:
                    print(f"Rectangle {selectedRect} got selected!")
                    if rectangles[selectedRect][-1] != -1:
                        rectangles[selectedRect][-1] = -1
                    else:
                        rectangles[selectedRect][-1] = 2
            elif len(self.oldFingersOnScreen) == 1 and selectedRect == -1 and self.mightClickEvent and len(self.drawCursors[0]) > 6:
                #print("DRAW MODE ACTIVATED") 
                #print(self.drawCursors) #index 2 = oldest # index -1 = newest
                gesture, score = gr.recognize(self.drawCursors[0][2:], gr.preprocessed_templates, 250)
                if score > 0.85:
                    angle = self.calculate_angle([gr.resampled_points[0][0],gr.resampled_points[0][1]], [gr.resampled_points[3][0],gr.resampled_points[3][1]])
                    drawnGesture = gesture['name']
                    center = [self.normToPixel(sum(points[0] for points in gr.resampled_points)/32) ,self.normToPixel(sum(points[1] for points in gr.resampled_points)/32)]
                    if drawnGesture == 'Circle':
                        self.circles.append([center,\
                            self.normToPixel(math.dist((gr.resampled_points[0][0],gr.resampled_points[0][1]),(gr.resampled_points[15][0],gr.resampled_points[15][1])))/2,\
                                (random.randint(50, 255),random.randint(50, 255),random.randint(50, 255))])
                        pass
                    elif drawnGesture == 'Square':
                        self.rectangles.append([len(self.rectangles),\
                            center,\
                                    self.normToPixel(math.dist((gr.resampled_points[3][0],gr.resampled_points[3][1]),(gr.resampled_points[19][0],gr.resampled_points[19][1]))),\
                                        angle,\
                                            (random.randint(50, 255),random.randint(50, 255),random.randint(50, 255)),\
                                                2])
                        pass
                    elif drawnGesture == 'Triangle':
                        #CENTER, SIZE, ROTATION, COLOR
                        self.triangles.append([center,\
                            math.dist((self.normToPixel(gr.resampled_points[0][0]),self.normToPixel(gr.resampled_points[0][1])),\
                                (center[0],center[1]))*2,\
                                self.calculate_triangle_angle([gr.resampled_points[0][0],gr.resampled_points[0][1]], [gr.resampled_points[3][0],gr.resampled_points[3][1]]),\
                                    (random.randint(50, 255),random.randint(50, 255),random.randint(50, 255))])
                        pass
            self.mightClickEvent = False
            self.fingerAge = 0

        # select rectangle
        currentTouchedRects = [finger[1] for finger in currentFingersOnScreen]
        if len(np.unique(currentTouchedRects)) != 1:
            selectedRect = -1
        else:
            selectedRect = currentTouchedRects[0]
        
        if len(currentFingersOnScreen) == 1 and selectedRect == -1:
            self.drawCursors = oldCursors.copy()
            if len(self.oldFingersOnScreen) == 0:
                self.mightClickEvent = True
                
        if len(currentFingersOnScreen) == 1 and selectedRect != -1:
            scaling = 1
            self.fingerAge += 1
            if len(self.oldFingersOnScreen) == 0:
                self.mightClickEvent = True
            # Translation
            if len(vectors) > 0:
                self.rectangles[selectedRect][1][0] += vectors[0][1][0] * multiplier
                self.rectangles[selectedRect][1][1] += vectors[0][1][1] * multiplier
        elif len(currentFingersOnScreen) == 2 and selectedRect != -1:
            self.mightClickEvent = False
            self.fingerAge += 1
            if (len(currentFingersOnScreen[0]) < 4) or (len(currentFingersOnScreen[1]) < 4):
                return

            # compute finger mid point
            prevFingerMid = [(currentFingersOnScreen[0][-2][0] +
                              currentFingersOnScreen[1][-2][0]) / 2, (currentFingersOnScreen[0][-2][1] +
                                                                      currentFingersOnScreen[1][-2][1]) / 2]
            currentFingerMid = [(currentFingersOnScreen[0][-1][0] +
                                 currentFingersOnScreen[1][-1][0]) / 2, (currentFingersOnScreen[0][-1][1] +
                                                                         currentFingersOnScreen[1][-1][1]) / 2]
            # compute previous rectangle mid point
            prevRectangleMid = self.rectangles[selectedRect][1]

            # compute finger distance
            prevFingerDistance = math.dist((currentFingersOnScreen[0][-2][0], currentFingersOnScreen[0][-2][1]),
                                           (currentFingersOnScreen[1][-2][0], currentFingersOnScreen[1][-2][1]))
            currentFingerDistance = math.dist((currentFingersOnScreen[0][-1][0], currentFingersOnScreen[0][-1][1]),
                                              (currentFingersOnScreen[1][-1][0], currentFingersOnScreen[1][-1][1]))

            # compute incremental finger angle
            prevFingerAngle = self.calculate_angle((currentFingersOnScreen[0][-2][0], currentFingersOnScreen[0][-2][1]),
                                                   (currentFingersOnScreen[1][-2][0], currentFingersOnScreen[1][-2][1]))
            currentFingerAngle = self.calculate_angle((currentFingersOnScreen[0][-1][0], currentFingersOnScreen[0][-1][1]),
                                                      (currentFingersOnScreen[1][-1][0], currentFingersOnScreen[1][-1][1]))
            incrFingerAngle = currentFingerAngle - prevFingerAngle

            # compute scaling
            scaling = currentFingerDistance / prevFingerDistance

            # compute rotation matrix
            incrFingerAngleInRad = np.radians(incrFingerAngle)
            cos_theta = np.cos(incrFingerAngleInRad)
            sin_theta = np.sin(incrFingerAngleInRad)
            rotation_matrix = np.array(
                [[cos_theta, -sin_theta], [sin_theta, cos_theta]])

            # rotate + translate + scale rectangle center
            currentFingerMidInPx = np.array(
                [self.normToPixel(currentFingerMid[0]), self.normToPixel(currentFingerMid[1])])
            prevFingerMidInPx = np.array(
                [self.normToPixel(prevFingerMid[0]), self.normToPixel(prevFingerMid[1])])

            currentRectangleMid = currentFingerMidInPx + \
                scaling * \
                np.dot(rotation_matrix, np.array(
                    prevRectangleMid) - prevFingerMidInPx)

            self.rectangles[selectedRect][1][0] = currentRectangleMid[0]
            self.rectangles[selectedRect][1][1] = currentRectangleMid[1]

            # rotate rectangle
            self.rectangles[selectedRect][3] = self.rectangles[selectedRect][3] + \
                incrFingerAngle

            # scale rectangle
            self.rectangles[selectedRect][2] = (
                self.rectangles[selectedRect][2] * scaling)

        self.oldFingersOnScreen = currentFingersOnScreen.copy()

    def calculate_vector(self, point_a, point_b):
        distance = [point_a[0] - point_b[0], point_a[1] - point_b[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1] / norm]
        return [direction[0] * math.sqrt(2), direction[1] * math.sqrt(2)]

    def isPointInRectangle(self, point, rectangle):
        center_x = rectangle[1][0]
        center_y = rectangle[1][1]
        size = rectangle[2]

        left = center_x - size/2
        right = center_x + size/2
        top = center_y - size/2
        bottom = center_y + size/2

        x = self.normToPixel(point[0])
        y = self.normToPixel(point[1])

        return left <= x <= right and top <= y <= bottom

    def calculate_angle(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2

        # Calculate the differences in x and y coordinates
        delta_x = x2 - x1
        delta_y = y2 - y1

        # Calculate the angle using the arctan function
        angle_rad = math.atan2(delta_y, delta_x)
        angle_deg = math.degrees(angle_rad)

        # Ensure the angle is within the range of 0 to 360 degrees
        if angle_deg < 0:
            angle_deg += 360

        return angle_deg

    def calculate_triangle_angle(self, point1, point2):
            x1, y1 = point1
            x2, y2 = point2

            # Calculate the differences in x and y coordinates
            delta_x = x2 - x1
            delta_y = y2 - y1

            # Calculate the angle using the arctan function
            angle_rad = math.atan2(delta_y, delta_x)
            angle_deg = math.degrees(angle_rad)
            angle_deg -= 150
    
            return angle_deg
    def calculateVectors(self):
        vectors.clear()
        normalized_vectors.clear()
        for cursor in oldCursors:
            if len(cursor) > 3:
                normalized_tempVector = [None]
                normalized_tempVector[0] = cursor[0]
                tempVector = [None]
                tempVector[0] = cursor[0]
                for age in range(2, len(cursor)-1):
                    dx = cursor[age+1][0] - cursor[age][0]
                    dy = cursor[age+1][1] - cursor[age][1]

                    magnitude = math.sqrt(dx**2 + dy**2)

                    if magnitude != 0:
                        normalized_tempVector.insert(
                            1, (dx/magnitude, dy/magnitude))
                    tempVector.insert(1, (dx, dy))
                vectors.append(tempVector)
                normalized_vectors.append(normalized_tempVector)

    def addOldCursors(self, newCursors):
        global oldCursors

        currentCursors = []
        for newCursor in newCursors:
            if any([cursor[0] == newCursor.session_id for cursor in oldCursors]):
                for cursor in oldCursors:
                    if cursor[0] == newCursor.session_id:
                        cursor.append(newCursor.position)
                        currentCursors.append(cursor)
            else:
                # check if cursor starts inside an object
                touchedObjectId = -1
                for rect in self.rectangles:
                    if self.isPointInRectangle(newCursor.position, rect):
                        touchedObjectId = max(touchedObjectId, rect[0])

                # append cursor
                currentCursors.append(
                    [newCursor.session_id, touchedObjectId, newCursor.position])

        idx = np.argsort([cursor[0] for cursor in currentCursors])
        currentCursors = [currentCursors[i] for i in idx]
        oldCursors = currentCursors

    def normToPixel(self, norm):
        coordinates = int(norm * dim)
        return coordinates
    

client = TuioClient(("localhost", 3333))
t1 = Thread(target=client.start)
listener = MyListener()
t2 = Thread(target=listener.update)
client.add_listener(listener)
t1.start()
t2.start()
image = np.zeros((dim, dim, 3), dtype=np.uint8)
