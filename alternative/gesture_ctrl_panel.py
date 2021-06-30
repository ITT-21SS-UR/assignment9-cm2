from PyQt5 import QtWidgets

from gesture_model import GestureModel


# copied from previous task with modifications

# Author: Claudia, Martina
# Reviewer: Martina
class GestureWidget(QtWidgets.QWidget):
    BEGIN_TRAINING_TEXT = "Train gesture"
    NO_GESTURE_TEXT = "- no gesture detected -"

    def __init__(self):
        super().__init__()

        self.__gesture_model = GestureModel()
        self.__setup_layout()

    def __setup_layout(self):
        self.__layout = QtWidgets.QVBoxLayout()

        self.__setup_gesture_main_layout()
        self.__setup_prediction_layout()
        self.__setup_gesture_list()

        self.__connect_signals()
        self.setLayout(self.__layout)

    def __setup_gesture_main_layout(self):
        self.__setup_add_gesture()
        self.__setup_remove_gesture()
        self.__setup_training_label()
        self.__setup_training_button()
        self.__setup_retrain_gesture()

    def __setup_prediction_layout(self):
        # setup info text for prediction
        info_text = QtWidgets.QLabel()
        info_text.setWordWrap(True)
        info_text.setText("\nTrain some gestures for prediction.\n\n"
                          "Latest predicted gesture:")
        self.__layout.addWidget(info_text)

        # setup text for the predicted gesture
        self.__prediction_text = QtWidgets.QLabel()
        self.__prediction_text.setWordWrap(True)
        self.__prediction_text.setText(self.NO_GESTURE_TEXT)
        self.__layout.addWidget(self.__prediction_text)

    def __setup_training_label(self):
        train_text = QtWidgets.QLabel()
        train_text.setText("\nTraining")
        self.__layout.addWidget(train_text)

    def __setup_training_button(self):
        training_button = QtWidgets.QPushButton()
        training_button.setText(self.BEGIN_TRAINING_TEXT)
        training_button.clicked.connect(self.__training_button_clicked)
        self.__layout.addWidget(training_button)

    def __training_button_clicked(self):
        if self.__gesture_model.is_gestures_empty():
            self.__show_no_gesture_item_selected()
            return

        self.__gesture_model.add_training_data()

    def __setup_add_gesture(self):
        add_gesture_button = QtWidgets.QPushButton("Add gesture")
        add_gesture_button.clicked.connect(self.__add_gesture_button_clicked)
        self.__layout.addWidget(add_gesture_button)

    def __add_gesture_button_clicked(self):
        gesture_name, ok = QtWidgets.QInputDialog.getText(self, "Add new gesture", "new gesture name")

        if gesture_name:
            self.__gesture_model.add_gesture(gesture_name)

    def __is_gesture_item_selected(self):
        if self.__gesture_list.currentItem():
            return True

        return False

    def __show_no_gesture_item_selected(self):
        QtWidgets.QMessageBox.warning(self, "No gesture selected", "No gesture was selected.\n"
                                                                   "Please select or add a gesture.")

    def __setup_retrain_gesture(self):
        retrain_gesture_button = QtWidgets.QPushButton("Retrain gesture")
        retrain_gesture_button.clicked.connect(self.__retrain_gesture_button_clicked)
        self.__layout.addWidget(retrain_gesture_button)

    def __retrain_gesture_button_clicked(self):
        if not self.__is_gesture_item_selected():
            self.__show_no_gesture_item_selected()
            return

        self.__show_gesture_accept_retrain()

    def __setup_remove_gesture(self):
        remove_gesture_button = QtWidgets.QPushButton("Remove gesture")
        remove_gesture_button.clicked.connect(self.__remove_gesture_button_clicked)
        self.__layout.addWidget(remove_gesture_button)

    def __remove_gesture_button_clicked(self):
        if not self.__is_gesture_item_selected():
            self.__show_no_gesture_item_selected()
            return

        self.__show_gesture_accept_removal()

    def __setup_gesture_list(self):
        gesture_label = QtWidgets.QLabel()
        gesture_label.setText("\nGestures")
        self.__layout.addWidget(gesture_label)

        self.__gesture_list = QtWidgets.QListWidget()
        self.__gesture_list.itemSelectionChanged.connect(self.__selected_gesture_changed)
        self.__layout.addWidget(self.__gesture_list)

    def __selected_gesture_changed(self):
        if self.__gesture_model.is_gestures_empty():
            self.__gesture_model.set_selected_gesture_name(None)
            return

        self.__gesture_model.set_selected_gesture_name(self.__gesture_list.currentItem().text())

    def __connect_signals(self):
        self.__gesture_model.gesture_name_exists.connect(self.__show_gesture_name_exists)
        self.__gesture_model.gesture_item_added.connect(self.__add_gesture_item)
        self.__gesture_model.gesture_predicted.connect(self.__update_gesture_predicted)

    def __update_gesture_predicted(self, text):
        self.__prediction_text.setText(text)

    def __handle_gestures_added(self, gesture_names):
        for name in gesture_names:
            self.__add_gesture_item(name)

    def __add_gesture_item(self, gesture_name: str):
        gesture_item = QtWidgets.QListWidgetItem(gesture_name)
        self.__gesture_list.addItem(gesture_item)
        self.__gesture_list.setCurrentItem(gesture_item)

    def __show_gesture_name_exists(self, gesture_name: str):
        QtWidgets.QMessageBox.warning(self, "Gesture exists",
                                      "Gesture \"{}\" already exists. (-_-)".format(gesture_name))

    def __show_gesture_accept_removal(self):
        gesture_name = self.__gesture_list.currentItem().text()

        remove_reply = QtWidgets.QMessageBox.question(self, "Remove gesture", "Are you sure to remove gesture \"{}\".\n"
                                                                              "This action can't be undone."
                                                      .format(gesture_name))

        if remove_reply == QtWidgets.QMessageBox.Yes:
            self.__gesture_model.remove_gesture(gesture_name)
            self.__gesture_list.takeItem(self.__gesture_list.currentRow())

    def __show_gesture_accept_retrain(self):
        gesture_name = self.__gesture_list.currentItem().text()

        retrain_reply = QtWidgets.QMessageBox.question(self, "Retrain gesture",
                                                       "Are you sure to retrain gesture \"{}\".\n"
                                                       "All trained data of this gesture will be removed.\n"
                                                       "This action can't be undone."
                                                       .format(gesture_name))

        if retrain_reply == QtWidgets.QMessageBox.Yes:
            self.__gesture_model.retrain_gesture(gesture_name)

    def get_gesture_model(self):
        return self.__gesture_model

    def set_prediction_text(self, text):
        self.__prediction_text.setText(text)
