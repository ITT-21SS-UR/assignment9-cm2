import sys
import math 
from PyQt5 import uic, Qt, QtWidgets
# from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QFont, QPen, QCursor, QPalette

# Author: Martina
# Reviewer and UI specialist: Claudia

# Explanation: Only drawing inside the white surface

class DrawGesture(QtWidgets.QWidget):
    def __init__(self):
        super(DrawGesture, self).__init__()
        uic.loadUi("gesture.ui", self)

        # start tracking the mouse so mouse move event gets called (needs widget to work on)
        self.setMouseTracking(True)

        # variables
        self.startPoint = (300,30)
        self.endPoint = (0,0)
        self.pressed = False
        self.allLinesArray = ([])
        self.allGestures = (["eins"], [230.09057192513646, 158.7213424488092], [233.3095939694985, 156.94017753523002], [230.0, 159.49987643021984], [233.3095939694985, 156.94017753523002], [237.0507220325263, 154.66660209338528], [237.04052208421933, 155.36459427022697], [241.04662441494824, 151.15454322978587], [241.014533571536, 151.89420791051663], [245.2276008519681, 147.85320514942896], [245.2276008519681, 148.52921667606418], [249.9703185026196, 143.3016924326351], [249.94973526889004, 144.05063292635282], [257.09049334826454, 137.93302353095083], [257.07326152127166, 138.6694595597187], [263.7888845543245, 132.5044513186342], [263.7888845543245, 133.18046284526946], [268.56360147600606, 127.97592327447211], [268.5296783948073, 128.73929636456768], [274.06985137735336, 123.85891734407862], [274.0931486948871, 124.48415160342529], [276.9320410596994, 120.29760678177738], [280.04877728146516, 116.23007705686271], [280.1059592208644, 116.78493560467133], [281.81413756033135, 112.98080779236787], [283.5988763778656, 110.48217344781989], [284.49185483772203, 110.01674221770243], [284.6178494915863, 110.0], [284.92573722208294, 111.83936503561517], [286.82477881619036, 113.46693436567953], [284.568789458576, 115.76579043419056], [286.4622734440518, 118.43388067900786], [286.4000248112876, 118.04918673844098], [285.7441775122261, 121.98345930811934], [285.03028198521235, 125.19598917968102], [284.3333049155751, 128.51033465724262], [283.94188534088016, 131.5537281247298], [283.87550223258063, 131.1148266033576], [282.8289628763569, 135.0096390343736], [281.478825539468, 138.51531928855923], [281.11120158068707, 142.00890604180216], [281.05708159989047, 141.65095434162248], [278.5006774789596, 146.10635033227317], [280.40311828553695, 149.54062566201463], [279.68771434661403, 154.52772623714839], [279.6461071442993, 154.2146266789929], [278.96371432376765, 159.1131026042666], [277.90297552907975, 164.16531585183344], [277.86136832676505, 163.85221629367794], [275.28814760739783, 168.9510071967118], [275.28814760739783, 173.59132812230092], [275.28814760739783, 178.23164904789002], [275.31110584794817, 178.43990419872637], [275.28814760739783, 182.51502220997224], [275.28814760739783, 186.0844998450408], [275.28814760739783, 189.29702971660248], [275.28814760739783, 192.50955958816417], [275.28814760739783, 195.36514169621898], [275.28814760739783, 197.86377604076696], [275.28814760739783, 200.36241038531494], [275.28814760739783, 203.2179924933698], [275.30115535186656, 205.15990079837397], [275.6450953709047, 207.50136565545202], [275.6450953709047, 209.2861044729863], [275.6450953709047, 210.0])

        # setup buttons
        self.setupButtons()

        self.__setup_gesture_list()
        self.__is_training = False  # TODO in model

    def addGesture(self):
        gesture_name, ok = QtWidgets.QInputDialog.getText(self, "Add new gesture", "new gesture name")

        if gesture_name and self.allLinesArray is not None:
            # TODO add gesture to list model
            self.__add_gesture_item(gesture_name)
            self.allGestures.append(gesture_name, self.newPoints)
            self.newPoints = ([])
            # self.__gesture_model.add_gesture(gesture_name)

    def clear(self):
        self.allLinesArray = ([])
        self.startPoint == (0,0)
        self.newPoints = ([])
        self.update()

    def recognize(self):
        self.OneDollarAlgorithm()
        representingSymbol = self.compareArrays()
        if representingSymbol is not None:
            print("representingSymbol: ", representingSymbol)
            
        # self.gestureRecognizeLabel text anpassen

    def setupButtons(self):
        self.addButton.clicked.connect(self.addGesture)
        self.emptyButton.clicked.connect(self.clear)
        self.recoButton.clicked.connect(self.recognize)
        self.deleteButton.clicked.connect(self.__delete_gesture_clicked)

    def __setup_gesture_list(self):
        self.gestureList.itemSelectionChanged.connect(self.__selected_gesture_changed)

    def getLength(self):
        distance = 0
        for element in self.allLinesArray:
            distancePoints = math.sqrt(abs(element[0] - element[2]) + abs (element[1] - element[3]))
            distance = distance + distancePoints
        return distance

    def getLowestPoint(self):
        lowestPoint = 0
        for element in self.newPoints:
            if element[1] > lowestPoint:
                lowestPoint = element[1]
        return lowestPoint

    def getHighestPoint(self):
        highestPoint = self.lineBottom.y()
        for element in self.newPoints:
            if element[1] < highestPoint:
                highestPoint = element[1]
        return highestPoint 

    def getRightPoint(self):
        rightPoint = 0
        for element in self.newPoints:
            if element[0] > rightPoint:
                rightPoint = element[0]
        return rightPoint

    def getLeftPoint(self):
        leftPoint = self.lineRight.x()
        for element in self.newPoints:
            if element[0] < leftPoint:
                leftPoint = element[0]
        return leftPoint

    def subdividePointsInto64(self):
        length = self.getLength()
        stepSize = length / 64
        # get points where this distance is between
        self.distance = 0
        self.newPoints = ([])
        counter = 0
        for element in self.allLinesArray:
            distanceFirst = math.sqrt(abs(element[0] - element[2]) + abs (element[1] - element[3]))
            self.distance = self.distance + distanceFirst
            firstGoThrough = True
            while self.distance > stepSize:
                # the loop goes until all points in that distance are created
                self.distance = self.distance - stepSize
                # from the first point in step size distance to the second point create a new point
                if firstGoThrough == True:
                    # mathematic understanding with the help of: 
                    # https://www.geeksforgeeks.org/find-points-at-a-given-distance-on-a-line-of-given-slope/
                    # don't divide through 0
                    if element[1] - element[3] == 0:
                        slope = 0
                    else:
                        slope = (element[0] - element[2]) / (element[1] - element[3])
                    if element[0] > element[2]:
                        x = element[0] + stepSize * math.sqrt(1 / (1 + slope*slope))
                    else:
                        x = element[0] - stepSize * math.sqrt(1 / (1 + slope*slope))
                    if element[1] > element[3]:
                        y = abs(element[1] - slope * stepSize * math.sqrt(1 / (1 + slope*slope)))
                    else:
                        y = abs(element[1] + slope * stepSize * math.sqrt(1 / (1 + slope*slope)))
                    firstGoThrough = False
                # else, during the second go through and those which follow, don't use the points from the original array, but use the one previously created ones in this loop
                else:
                    if self.newPoints[(len(self.newPoints) - 1)][1] - element[3] == 0:
                        slope = 0
                    else:
                        slope = (self.newPoints[(len(self.newPoints) - 1)][0] - element[2]) / (self.newPoints[(len(self.newPoints) - 1)][1] - element[3])
                    if self.newPoints[(len(self.newPoints) - 1)][0] > element[2]:
                        x = element[0] + stepSize * math.sqrt(1 / (1 + slope*slope))
                    else:
                        x = element[0] - stepSize * math.sqrt(1 / (1 + slope*slope))
                    if self.newPoints[(len(self.newPoints)- 1)][1] > element[3]:
                        y = abs(self.newPoints[(len(self.newPoints) - 1)][1] - stepSize * slope *  math.sqrt(1 / (1 + slope*slope)))
                    else:
                        y = abs(self.newPoints[(len(self.newPoints) - 1)][1] + stepSize * slope * math.sqrt(1 / (1 + slope*slope)))
                # create new point and save it to a new array
                self.newPoints.append([x, y])
                distanceFirstPoint = 0

    def getCenteroid(self):
        sumX = 0
        sumY = 0
        for element in self.newPoints:
            sumX = sumX + element[0]
            sumY = sumY + element[1]
        xValue = sumX / len(self.newPoints)
        yValue = sumY / len(self.newPoints)
        return (xValue, yValue)

    def rotateAll(self):
        centeroid = self.getCenteroid()
        # shift centeroid to 0,0 point and all points with it
        for element in self.newPoints:
            element[0] = element[0] - centeroid[0]
            element[1] = element[1] - centeroid[1]
        # find angle alpha between centroid and first point, from the lecture:
        disX = self.newPoints[0][0] - centeroid[0]
        disY = self.newPoints[0][1] - centeroid[1]
        alpha = -math.atan2(disY, disX) * 180 / math.pi
        # rotate all points around center by -alpha 
        for element in self.newPoints:
            self.rotate_origin_only(element[0], element[1], alpha)

    # taken from https://gist.github.com/LyleScott/e36e08bfb23b1f87af68c9051f985302
    def rotate_origin_only(self, x, y, radians):
        #Only rotate a point around the origin (0, 0)
        xx = x * math.cos(radians) + y * math.sin(radians)
        yy = -x * math.sin(radians) + y * math.cos(radians)
        return xx, yy

    def scaleToBoundingBox(self):
        lowestPoint = self.getLowestPoint()
        highestPoint = self.getHighestPoint()
        rightPoint = self.getRightPoint()
        leftPoint = self.getLeftPoint()
        
        heightGesture = lowestPoint - highestPoint
        widthGesture = rightPoint - leftPoint
        
        if heightGesture > widthGesture:
            scaleFactor = heightGesture / 100
        else:
            scaleFactor = widthGesture / 100

        # apply scale factor to all points, for y as well as x factor
        if scaleFactor != 0:
            for element in self.newPoints:
                element[0] = element[0] / scaleFactor
                element[1] = element[1] / scaleFactor
        else:
            print("no height, therefore can't be number 1-3, please try again")
            
    def repositionGesture(self):
        # position should be at self.lineLeft.x() + 100
        optimalPosLeftPoint = self.lineLeft.x() + 100
        optimalPosTopPoint = self.lineTop.y() + 100
        highestPoint = self.getHighestPoint()
        leftPoint = self.getLeftPoint()
        
        shiftValueHorizontal = leftPoint - optimalPosLeftPoint
        shiftValueVertical = highestPoint - optimalPosTopPoint
        
        for element in self.newPoints:
            element[0] = element[0] - shiftValueHorizontal
            element[1] = element[1] - shiftValueVertical

    def OneDollarAlgorithm(self):
        self.subdividePointsInto64()
        if len(self.newPoints) > 0:
            self.scaleToBoundingBox()
            self.rotateAll()
            self.repositionGesture()

        ##################################Test##################################
        testlist = ([])
        for i in range(len(self.newPoints) - 2):
            testlist.append([self.newPoints[i+1][0], self.newPoints[i+1][1], self.newPoints[i][0], self.newPoints[i][1]])

        self.clear()
        self.allLinesArray = testlist

    def checkIfThisWasTheSymbol(rangeStart, rangeEnd):
        distance = 0
        i = 0
        for j in range(rangeStart, rangeEnd):
            # self.allGestures has 65 elements, as the name also has to be saved
            distance =  distance + math.sqrt(abs(self.newPoints[i][0] - self.allGestures[j][0]) + abs(self.newPoints[i][1] - self.allGestures[j][1]))
            i = i + 1
        return distance
    
    def compareArrays(self):-
        # compare to template
        # distance of less then 1000 counts as resembling the symbol
        distance = 1000
        for i in range(1, len(self.gestureList)):
            newDistance = checkIfThisWasTheSymbol(i*1, i*65)
            if newDistance < distance:
                return i
        return None
    
    def __selected_gesture_changed(self):
        print("selection changed")
        
        # TODO depending on data of gesture update gesture list model
        # self.gestureList.currentItem().text()

    def __add_gesture_item(self, gesture_name: str):
        gesture_item = QtWidgets.QListWidgetItem(gesture_name)
        self.gestureList.addItem(gesture_item)
        self.gestureList.setCurrentItem(gesture_item)

    def __delete_gesture_clicked(selfrepresentingSymbol):
        if not self.__is_gesture_item_selected():
            self.__show_no_gesture_item_selected()
            return

        self.__show_gesture_accept_delete()

    def __show_no_gesture_item_selected(self):
        QtWidgets.QMessageBox.warning(self, "No gesture selected", "No gesture was selected.\n"
                                                                   "Please select or add a gesture.")

    def __show_gesture_accept_delete(self):
        gesture_name = self.gestureList.currentItem().text()

        remove_reply = QtWidgets.QMessageBox.question(self, "Delete gesture", "Are you sure to delete gesture \"{}\".\n"
                                                                              "This action can't be undone."
                                                      .format(gesture_name))

        if remove_reply == QtWidgets.QMessageBox.Yes:
            # TODO remove from model list
            # self.__gesture_model.remove_gesture(gesture_name)
            self.gestureList.takeItem(self.gestureList.currentRow())

    def __is_gesture_item_selected(self):
        if self.gestureList.currentItem():
            return True
            
        return False

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QPen(QColor(0, 0, 0, 255), 3))
        # redraw old lines 
        for element in self.allLinesArray:
            qp.drawLine(element[0], element[1], element[2], element[3])
        # end the painter
        qp.end()

    def insideCanvas(self, x, y):
        # the draw area is defined by 4 lines (lineTop, lineLeft, lineRight, lineBottom)
        if y > self.lineTop.y() and y < self.lineBottom.y() and x > self.lineLeft.x() and x < self.lineRight.x():
            return True
        else:
            return False

    def mousePressEvent(self, event):
        if self.insideCanvas(event.x(), event.y()):
            self.startPoint = (event.x(), event.y())
            self.pressed = True

    def mouseReleaseEvent(self, event):
        if self.insideCanvas(event.x(), event.y()):
            self.startPoint = (event.x(), event.y())
            self.pressed = False

    def mouseMoveEvent(self, event):
        if self.pressed == True and self.insideCanvas(event.x(), event.y()):
            self.endPoint = (event.x(), event.y())
            self.update()
            self.allLinesArray.append([self.startPoint[0], self.startPoint[1], self.endPoint[0], self.endPoint[1]])
            self.startPoint = (event.x(), event.y())


def main():
    # constructs an application object and window
    app = Qt.QApplication(sys.argv)

    # create a Class Object
    drawing = DrawGesture()
    drawing.show()

    # enter main event loop until application is exited or destroyed
    app.exec()


if __name__ == '__main__':
    main()
