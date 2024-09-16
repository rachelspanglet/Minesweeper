# imports
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from random import *
import sys

# global vars for game settings
LENGTH = 10
WIDTH = 10
MINES = 3
GRID = []

# class for a square in the game and its related features
class Square(QPushButton):
    def __init__(self, window, x, y):
        super().__init__(parent=window)
        self.state = "Safe"
        self.number = 0
        self.x = x
        self.y = y
        self.uncovered = False
        self.clicked.connect(self.clickHandle)
        self.setStyleSheet("padding: 0; margin: 0;")
        self.flagged = False
        self.setStyleSheet("background-color: #E1E1E1;")

    # handle all clicks on the square
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton: # right
            self.rightClickHandle()
        else: # left
            self.clickHandle()
    # determine how many flags are adjacent to the square
    def adjacentFlags(self):
        num = 0
        # check surrounding squares in grid matrix
        for i in range(self.x-1, self.x+2):
            for j in range(self.y-1, self.y+2):
                try:
                    if i >= 0 and j >= 0 and GRID[i][j].flagged and (i != self.x or j != self.y):
                        num += 1
                except:
                    pass
        return num
    # handle left clicks on square
    def clickHandle(self):
        global GRID
        if self.state == "Safe" and self.uncovered and self.adjacentFlags() >= self.number:
            for i in range(self.x-1, self.x+2):
                for i in range(self.x-1, self.x+2):
                            for j in range(self.y-1, self.y+2):
                                try:
                                    if i >= 0 and j >= 0 and not GRID[i][j].uncovered and not GRID[i][j].flagged and (i != self.x or j != self.y):
                                        GRID[i][j].clickHandle()
                                except:
                                    pass

        elif self.state == "Safe" and self.number == 0: # safe blank square
            self.setEnabled(False)
            self.setStyleSheet("background - color : #787878")
            self.uncover()
        elif self.state == "Safe": # safe non-blank square
            self.setText(str(self.number))
            self.setStyleSheet("background-color: #787878;")
            self.uncovered = True
            print(self.text(), self.state)
        elif self.state == "Mine": # square is a mine
            print("mine")
            endGame(self)

    # handle right clicks on the square
    def rightClickHandle(self):
        if not self.uncovered and not self.flagged:
            self.setIcon(QIcon('flag.png'))
            self.setIconSize(QSize(40, 36))
            self.flagged = True
        elif not self.uncovered:
            self.setIcon(QIcon())
            self.flagged = False
            
    # determine how to display a square once uncovered
    def showSquare(self):
        global GRID
        if self.state == "Safe" and self.number == 0: # blank square
            self.setEnabled(False)
            self.setStyleSheet("background-color: #787878;")
        elif self.state == "Safe": # non-blank square
            self.setText(str(self.number))
            self.setStyleSheet("background-color: #787878;")
            print(self.text(), self.state)

    # determine how many mines are adjacent to square
    def getNumber(self):
        global GRID
        num = 0
        for i in range(self.x-1, self.x+2):
            for j in range(self.y-1, self.y+2):
                try:
                    if i >= 0 and j >= 0 and GRID[i][j].state == "Mine" and (i != self.x or j != self.y):
                        num += 1
                except:
                    pass
        self.number = num
        return num

    # method for uncovering the state of square to user
    def uncover(self):
        self.uncovered = True
        if self.state == "Safe" and self.number == 0: # recursively uncover all adjacent squares given a 0-mine tile
            self.showSquare()
            for i in range(self.x-1, self.x+2):
                for j in range(self.y-1, self.y+2):
                    try:
                        if i >= 0 and j >= 0 and GRID[i][j].state == "Safe" and (i != self.x or j != self.y) and not GRID[i][j].uncovered:
                            GRID[i][j].uncover()
                    except:
                        pass
        elif self.state == "Safe":
            self.showSquare()

# end game due to clicking a bad square
def endGame(mine):
    global GRID
    global LENGTH
    global WIDTH
    for i in range(LENGTH):
        for j in range(WIDTH):
            if GRID[i][j].state == "Mine":
                GRID[i][j].setIcon(QIcon('mine.jpg'))
                GRID[i][j].setIconSize(QSize(40, 36))
            GRID[i][j].setEnabled(False)
    mine.setStyleSheet("background-color: red;")

# main function
def runGame():
    global GRID
    global LENGTH
    global WIDTH
    global MINES
    choices = []
    gr = QGridLayout()
    gr.setContentsMargins(0, 0, 0, 0)
    gr.setSpacing(0)
    for i in range(LENGTH):
        row = []
        for j in range(WIDTH):
            square = Square(window, i, j)
            square.show()
            row.append(square)
            gr.addWidget(square, i, j)
            square.setFixedSize(40, 40)
            choices.append([i, j])
        GRID.append(row)

    for i in range(MINES):
        print(MINES)
        rand = randint(0, len(choices)-1)
        choice = choices[rand]
        GRID[choice[0]][choice[1]].state = "Mine"
        choices.remove(choices[rand])

    for i in range(LENGTH):
        for j in range(WIDTH):
            GRID[i][j].getNumber()
    window.setLayout(gr)
    print("done")

# initialize vars and run the game
if __name__ == "__main__":
    LENGTH = 23
    WIDTH = 23
    MINES = 100
    GRID = []
    app = QApplication([])
    window = QWidget()
    window.setFixedHeight(LENGTH*40)
    window.setFixedWidth(WIDTH*40)
    window.setWindowTitle("Minesweeper")
    runGame()
    #print(GRID)
    window.show()
    sys.exit(app.exec())
    

