import sys

from PyQt5 import Qt, QtWidgets

from QDrawWidget import QDrawWidget
from gesture_ctrl_panel import GestureWidget


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
        self.__layout = QtWidgets.QHBoxLayout()

        self.__ctrl_panel = GestureWidget()
        self.__layout.addWidget(self.__ctrl_panel)

        # TODO setup draw file
        self.__draw_widget = QDrawWidget()
        self.__layout.addWidget(self.__draw_widget)

        self.setLayout(self.__layout)


def main():
    app = Qt.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
