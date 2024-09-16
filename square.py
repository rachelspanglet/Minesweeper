from PyQt6.QtWidgets import *
from game import *

class Square(QPushButton):
    def __init__(self, window):
        super().__init__(parent=window)
        self.resize(5, 5)
        self.state = "Safe"
        self.number = 0
        self.clicked.connect(self.clickHandle)
        self.setStyleSheet("background - color : #E1E1E1")

    def clickHandle(self):
        global GRID
        if self.state == "Safe" and self.number == 0:
            self.setEnabled(False)
            self.setStyleSheet("background - color : #787878")
        elif self.state == "Safe":
            self.setEnabled(False)
            self.setText(str(self.number))
            self.setStyleSheet("background - color : #787878")
        else:
            endGame(self)
