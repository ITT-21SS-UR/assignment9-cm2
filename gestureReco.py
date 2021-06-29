import sys
from PyQt5 import uic, Qt, QtWidgets
# from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QFont, QPen, QCursor, QPalette

# Author: Martina
# Reviewer:  Claudia

# Explanation: Only drawing inside the white surface

class DrawGesture(QtWidgets.QWidget):
    def __init__(self):
        super(DrawGesture, self).__init__()
        uic.loadUi("gesture.ui", self) 
        self.show()
        
        # start tracking the mouse so mouse move event gets called (needs widget to work on)
        self.setMouseTracking(True)
        
        # variables
        self.startPoint = (300,30)
        self.endPoint = (0,0)
        self.pressed = False
        self.allLinesArray = ([])
        
        # setup buttons
        self.setupButtons()

    def addImage(self):
        print("add Button pressed")

    def clear(self):
        self.allLinesArray = ([])
        self.startPoint == (0,0)
        self.update()
        print("clear Button pressed")

    def recognize(self):
        print("reco Button pressed")

    def setupButtons(self):
        self.addButton.clicked.connect(lambda value: self.addImage())
        self.emptyButton.clicked.connect(lambda value: self.clear())
        self.recoButton.clicked.connect(lambda value: self.recognize())

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QPen(QColor(0, 0, 0, 255), 3))
        # redraw old lines 
        for element in self.allLinesArray:
            qp.drawLine(element[0], element[1], element[2], element[3])
        # end the painter
        qp.end()
        self.show()
        
    def insideCanvas(self, x, y):
        # the draw area is defined by 4 lines (lineTop, lineLeft, lineRight, lineBottom)
        if y > self.lineTop.y() and y < self.lineBottom.y() and x > self.lineLeft.x() and x < self.lineRight.x(): 
            return True
        else:
            return False
        
    def mousePressEvent(self, event):
        if self.insideCanvas(event.x(), event.y()):
            self.startPoint = (event.x(), event.y())
            print("changed", self.startPoint)
            print("event.x()", event.x())
            print("event.y()", event.y())
            self.pressed = True
        
    def mouseReleaseEvent(self, event): 
        if self.insideCanvas(event.x(), event.y()):
            self.startPoint = (event.x(), event.y())
            print("changed", self.startPoint)
            print("event.x()", event.x())
            print("event.y()", event.y())
            self.pressed = False
          
    def mouseMoveEvent(self, event):
        if self.pressed == True and self.insideCanvas(event.x(), event.y()):
            self.endPoint = (event.x(), event.y())
            self.update()
            print("end, ", self.endPoint)
            print("startPoint, ", self.startPoint)
            self.allLinesArray.append([self.startPoint[0], self.startPoint[1], self.endPoint[0], self.endPoint[1]])
            self.startPoint = (event.x(), event.y())


def main():
    # constructs an application object and window
    app = Qt.QApplication(sys.argv)

    # create a Class Object
    drawinf = DrawGesture()

    # enter main event loop until application is exited or destroyed
    app.exec()


if __name__ == '__main__':
    main()
