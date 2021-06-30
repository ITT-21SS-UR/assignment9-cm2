from enum import Enum

from PyQt5.QtCore import QObject, pyqtSignal


class GestureState(Enum):
    INACTIVE = "inactive"
    TRAINING = "training"
    PREDICTION = "predict"


class GestureModel(QObject):
    GESTURE_NAME = "gesture_name"
    GESTURE_DATA = "gesture_data"
    GESTURE_ID = "id"

    state_changed = pyqtSignal([GestureState])
    gesture_name_exists = pyqtSignal([str])
    gesture_item_added = pyqtSignal([str])

    def __init__(self):
        super().__init__()

        self.__gestures = []
        self.__id_count = 0
        self.__gesture_state = GestureState.INACTIVE
        self.__is_training = False
        self.__selected_gesture_name = None

    def __exists_gesture_name(self, gesture_name: str):
        for gesture in self.__gestures:
            if gesture[self.GESTURE_NAME] == gesture_name:
                return True

        return False

    def __find_gesture_by_name(self, gesture_name):
        return next((gesture for gesture in self.__gestures if gesture[self.GESTURE_NAME] == gesture_name), None)

    def __add_gesture_name_to_gestures(self, gesture_name):
        self.__gestures.append({self.GESTURE_ID: self.__id_count,
                                self.GESTURE_NAME: gesture_name,
                                self.GESTURE_DATA: []})
        self.__id_count += 1

    def add_gesture(self, gesture_name: str):
        if self.__exists_gesture_name(gesture_name):
            self.gesture_name_exists.emit(gesture_name)
            return

        self.__add_gesture_name_to_gestures(gesture_name)

        self.gesture_item_added.emit(gesture_name)

    def remove_gesture(self, gesture_name: str):
        self.__gestures = [gesture for gesture in self.__gestures if not (gesture[self.GESTURE_NAME] == gesture_name)]

        if self.is_gestures_empty():
            self.__selected_gesture_name = None

        self.train_gestures()  # all gestures have to be trained again

    def is_gestures_empty(self):
        return not self.__gestures

    def get_gesture_state(self):
        return self.__gesture_state

    def set_gesture_state(self, state):
        self.__gesture_state = state
        self.state_changed.emit(state)

    def set_selected_gesture_name(self, gesture_name):
        self.__selected_gesture_name = gesture_name

    def is_training(self):
        return self.__is_training

    def set_is_training(self, is_training):
        self.__is_training = is_training

    def collect_training_data(self, gesture_input):
        # TODO
        if not self.__is_training:
            return

        # selected_gesture = self.__find_gesture_by_name(self.__selected_gesture_name)
        # selected_gesture[self.GESTURE_DATA].append(gesture_input[NodeKey.GESTURE_DATA.value])

    def train_gestures(self):
        print("train gesture")
        pass

    def predict_gesture(self, gesture_input):
        print("predict")
        pass
