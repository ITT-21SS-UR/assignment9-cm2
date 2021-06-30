import sys

from PyQt5 import Qt, QtWidgets

from QDrawWidget import QDrawWidget
from gesture_ctrl_panel import GestureWidget

"""
QDrawWidget.py and dollar_1.py are copied from the course resources with some adjustments. 
"""


# Author: Martina, Claudia
# Reviewer:  Claudia
class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.__setup_main_window()
        self.__setup_components()

    def __setup_main_window(self):
        self.setWindowTitle("$1 Gesture Recognizer")
        self.move(QtWidgets.qApp.desktop().availableGeometry(
            self).center() - self.rect().center())
        self.setMinimumSize(900, 600)

    def __setup_components(self):
        layout = QtWidgets.QHBoxLayout()

        self.__ctrl_panel = GestureWidget()
        layout.addWidget(self.__ctrl_panel)

        self.__draw_widget = QDrawWidget()
        layout.addWidget(self.__draw_widget)
        self.__draw_widget.drawing_finished.connect(self.__predict_gesture)

        self.setLayout(layout)

    def __predict_gesture(self):
        if self.__ctrl_panel.get_gesture_model().is_gestures_empty():
            self.__ctrl_panel.set_prediction_text("- no gesture was trained -")

        try:
            self.__ctrl_panel.get_gesture_model().update_current_gesture_input(self.__draw_widget.points)
            predicted_gesture = self.__ctrl_panel.get_gesture_model().predict_gesture(self.__draw_widget.points)

            if predicted_gesture:
                self.__ctrl_panel.set_prediction_text(predicted_gesture)

        except ZeroDivisionError:
            sys.stderr.write("ZeroDivisionError")


def main():
    app = Qt.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
