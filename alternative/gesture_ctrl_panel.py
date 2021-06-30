from PyQt5 import QtWidgets

from gesture_model import GestureModel, GestureState


# copied from previous task with modifications
class GestureWidget(QtWidgets.QWidget):
    BEGIN_TRAINING_TEXT = "Begin Training"
    TRAINING_TEXT = "Training..."

    def __init__(self):
        super().__init__()

        self.__gesture_model = GestureModel()
        self.__setup_layout()

    def __setup_layout(self):
        self.__layout = QtWidgets.QVBoxLayout()

        self.__setup_gesture_state_selection_layout()
        self.__setup_gesture_button_layout()
        self.__setup_info_text()
        self.__setup_training_button()
        self.__setup_gesture_list()

        # was added here because the training button should appear after the info text
        # so that no error occurs when the training button is hidden/shown
        self.__handle_state_changed(self.__gesture_model.get_gesture_state())

        self.__connect_signals()
        self.setLayout(self.__layout)

    def __setup_gesture_state_selection_layout(self):
        self.__state_selection_layout = QtWidgets.QVBoxLayout()

        self.__setup_state_label()
        self.__setup_inactive_button()
        self.__setup_select_training_button()
        self.__setup_prediction_button()

        self.__layout.addLayout(self.__state_selection_layout)

    def __setup_state_label(self):
        state_label = QtWidgets.QLabel()
        state_label.setText("State")
        self.__state_selection_layout.addWidget(state_label)

    def __setup_select_training_button(self):
        self.__select_training_button = QtWidgets.QRadioButton(GestureState.TRAINING.value)
        self.__select_training_button.clicked.connect(self.__select_training_button_clicked)
        self.__state_selection_layout.addWidget(self.__select_training_button)

    def __select_training_button_clicked(self):
        self.__select_training_button.setChecked(True)
        self.__gesture_model.set_gesture_state(GestureState.TRAINING)

    def __setup_prediction_button(self):
        self.__prediction_button = QtWidgets.QRadioButton(GestureState.PREDICTION.value)
        self.__prediction_button.clicked.connect(self.__prediction_button_clicked)
        self.__state_selection_layout.addWidget(self.__prediction_button)

    def __prediction_button_clicked(self):
        self.__gesture_model.set_gesture_state(GestureState.PREDICTION)

    def __setup_inactive_button(self):
        self.__inactive_button = QtWidgets.QRadioButton(GestureState.INACTIVE.value)
        self.__inactive_button.clicked.connect(self.__inactive_button_clicked)
        self.__inactive_button.setChecked(True)
        self.__state_selection_layout.addWidget(self.__inactive_button)

    def __inactive_button_clicked(self):
        self.__gesture_model.set_gesture_state(GestureState.INACTIVE)

    def __setup_gesture_button_layout(self):
        self.__gesture_button_layout = QtWidgets.QVBoxLayout()

        self.__setup_add_gesture()
        self.__setup_retrain_gesture()
        self.__setup_remove_gesture()

        self.__layout.addLayout(self.__gesture_button_layout)

    def __setup_info_text(self):
        self.__info_text = QtWidgets.QLabel()
        self.__info_text.setWordWrap(True)
        self.__layout.addWidget(self.__info_text)

    def __handle_state_changed(self, state):
        self.__handle_stop_training()

        if state == GestureState.TRAINING:
            self.__info_text.setText("To train your gesture click \"{}\".\n"
                                     "Click on \"{}\" to stop the training.".format(self.BEGIN_TRAINING_TEXT,
                                                                                    self.TRAINING_TEXT))
            self.__training_button.show()

        elif state == GestureState.PREDICTION:
            self.__info_text.setText("Predicted gesture is shown in DisplayText.\n"
                                     "A minimum of 2 trained gestures is required for correct prediction.")
            self.__training_button.hide()

        elif state == GestureState.INACTIVE:
            self.__info_text.setText("Select another state to train or predict a gesture.")
            self.__training_button.hide()

    def __handle_stop_training(self):
        self.__training_button.setText(self.BEGIN_TRAINING_TEXT)
        self.__gesture_model.train_gestures()

    def __setup_training_button(self):
        self.__training_button = QtWidgets.QPushButton()
        self.__training_button.setText(self.BEGIN_TRAINING_TEXT)
        self.__training_button.clicked.connect(self.__training_button_clicked)
        self.__layout.addWidget(self.__training_button)

    def __training_button_clicked(self):
        if self.__gesture_model.is_training():
            self.__handle_stop_training()
        else:
            if self.__gesture_model.is_gestures_empty():
                self.__show_no_gesture_item_selected()
                return

            self.__training_button.setText(self.TRAINING_TEXT)
            self.__gesture_model.set_is_training(True)

    def __setup_add_gesture(self):
        self.__add_gesture_button = QtWidgets.QPushButton("Add gesture")
        self.__add_gesture_button.clicked.connect(self.__add_gesture_button_clicked)
        self.__gesture_button_layout.addWidget(self.__add_gesture_button)

    def __add_gesture_button_clicked(self):
        self.__handle_stop_training()
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
        self.__retrain_gesture_button = QtWidgets.QPushButton("Retrain gesture")
        self.__retrain_gesture_button.clicked.connect(self.__retrain_gesture_button_clicked)
        self.__gesture_button_layout.addWidget(self.__retrain_gesture_button)

    def __retrain_gesture_button_clicked(self):
        self.__handle_stop_training()

        if not self.__is_gesture_item_selected():
            self.__show_no_gesture_item_selected()
            return

        self.__show_gesture_accept_retrain()

    def __setup_remove_gesture(self):
        self.__remove_gesture_button = QtWidgets.QPushButton("Remove gesture")
        self.__remove_gesture_button.clicked.connect(self.__remove_gesture_button_clicked)
        self.__gesture_button_layout.addWidget(self.__remove_gesture_button)

    def __remove_gesture_button_clicked(self):
        self.__handle_stop_training()

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
        self.__handle_stop_training()

        if self.__gesture_model.is_gestures_empty():
            return

        self.__gesture_model.set_selected_gesture_name(self.__gesture_list.currentItem().text())

    def __connect_signals(self):
        self.__gesture_model.gesture_name_exists.connect(self.__show_gesture_name_exists)
        self.__gesture_model.gesture_item_added.connect(self.__add_gesture_item)
        self.__gesture_model.state_changed.connect(self.__handle_state_changed)

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
            self.__select_training_button_clicked()

    def get_gesture_model(self):
        return self.__gesture_model
