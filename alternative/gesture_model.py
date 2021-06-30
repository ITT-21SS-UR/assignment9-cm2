from PyQt5.QtCore import QObject, pyqtSignal


# copied from previous task with modifications

# Author: Claudia, Martina
# Reviewer:  Martina

class GestureModel(QObject):
    GESTURE_NAME = "gesture_name"
    GESTURE_DATA = "gesture_data"
    GESTURE_ID = "id"

    gesture_name_exists = pyqtSignal([str])
    gesture_item_added = pyqtSignal([str])

    def __init__(self):
        super().__init__()

        self.__gestures = []
        self.__id_count = 0
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

    def set_selected_gesture_name(self, gesture_name):
        self.__selected_gesture_name = gesture_name

    def add_training_data(self, gesture_input):
        # TODO add_training_data
        # selected_gesture = self.__find_gesture_by_name(self.__selected_gesture_name)
        # selected_gesture[self.GESTURE_DATA].append(gesture_input[NodeKey.GESTURE_DATA.value])
        pass

    def train_gestures(self):
        # TODO train gestures
        print("train")

    def predict_gesture(self, gesture_input):
        # TODO predict gesture
        print("predict")

    def retrain_gesture(self, gesture_name):
        # TODO delete if not enough time to implement
        print("retrain")
        self.train_gestures()  # all gestures have to be trained again
