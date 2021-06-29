import sys
from PyQt5 import uic, Qt, QtWidgets
# from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QFont, QPen, QCursor, QPalette

# Author: Martina
# Reviewer: Claudia

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

        # setup buttons
        self.setupButtons()

        self.__setup_gesture_list()
        self.__is_training = False  # TODO in model

    def addImage(self):
        self.__handle_stop_training()
        gesture_name, ok = QtWidgets.QInputDialog.getText(self, "Add new gesture", "new gesture name")

        if gesture_name:
            # TODO add gesture to list model
            self.__add_gesture_item(gesture_name)
            # self.__gesture_model.add_gesture(gesture_name)

    def clear(self):
        self.allLinesArray = ([])
        self.startPoint == (0,0)
        self.update()
        print("clear Button pressed")

    def recognize(self):
        self.__handle_stop_training()
        # TODO at least ?? gesture have to be trained for recognition
        # self.gestureRecognizeLabel text anpassen
        print("reco Button pressed")

    def setupButtons(self):
        self.addButton.clicked.connect(self.addImage)
        self.emptyButton.clicked.connect(self.clear)
        self.recoButton.clicked.connect(self.recognize)
        self.deleteButton.clicked.connect(self.__delete_gesture_clicked)
        self.trainButton.clicked.connect(self.__train_gesture_clicked)

    def __setup_gesture_list(self):
        self.gestureList.itemSelectionChanged.connect(self.__selected_gesture_changed)

    def __selected_gesture_changed(self):
        print("selection changed")
        # TODO depending on data of gesture update gesture list model
        # self.gestureList.currentItem().text()

    def __add_gesture_item(self, gesture_name: str):
        gesture_item = QtWidgets.QListWidgetItem(gesture_name)
        self.gestureList.addItem(gesture_item)
        self.gestureList.setCurrentItem(gesture_item)

    def __delete_gesture_clicked(self):
        self.__handle_stop_training()
        if not self.__is_gesture_item_selected():
            self.__show_no_gesture_item_selected()
            return

        self.__show_gesture_accept_delete()

    def __train_gesture_clicked(self):
        if not self.__is_gesture_item_selected():
            self.__show_no_gesture_item_selected()
            return

        if self.__is_training:
            self.__handle_stop_training()
        else:
            self.trainButton.setText("Training...")
            self.__is_training = True  # TODO in model
            # TODO collect training data
            # self.__gesture_model.set_is_training(True)

    def __handle_stop_training(self):
        self.trainButton.setText("Train Gesture")
        self.__is_training = False  # TODO in model
        # self.__gesture_model.train_gestures()

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
    drawinf.show()

    # enter main event loop until application is exited or destroyed
    app.exec()


if __name__ == '__main__':
    main()
