import math
import random

from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt
import sys
import time
import threading
from threading import Thread


class PrincessWave(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(260, 20, 70, 70)
        pix = QPixmap('wave.png')
        pixx = pix.scaled(QSize(70, 70))
        self.setPixmap(pixx)

    def wave_function(self,):
        while 1:

         time.sleep(1)


class Princess(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(260, 20, 70, 70)
        pix = QPixmap('peach2.png')
        pixx = pix.scaled(QSize(70, 70))
        self.setPixmap(pixx)


class Mover(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 608, 70, 70)
        pix = QPixmap('ItsAMeRight.png')
        pixx = pix.scaled(QSize(70, 70))
        self.setPixmap(pixx)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.move(self.x(), self.y() - 15)
        elif event.key() == Qt.Key_Down:
            if self.y() + 15 <= 610:
                self.move(self.x(), self.y() + 15)
        elif event.key() == Qt.Key_Left:
            if self.x() - 5 >= -25:
                self.move(self.x() - 5, self.y())
                pix = QPixmap('ItsAMeLeft.png')
                pixx = pix.scaled(QSize(70, 70))
                self.setPixmap(pixx)
        elif event.key() == Qt.Key_Right:
            if self.x() + 5 <= 532:
                self.move(self.x() + 5, self.y())
                pix = QPixmap('ItsAMeRight.png')
                pixx = pix.scaled(QSize(70, 70))
                self.setPixmap(pixx)
        else:
            QLabel.keyPressEvent(self, event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def makeMap(self):
        for i in range(0, self._height // 15 + 1):
            row = []
            for j in range(0, self._width // 15):
                row.append(0)
            self.map.append(row)

    def makeWalls(self): # Wall = 1
        for i in range(0, (self._height // 15) - 4):
            self.map[i][0] = self.map[i][self._width // 15 - 1] = 1
        for i in range(0, (self._height // (15 * 5))):
            for j in range(0, self._width // 15):
                self.map[i * 5][j] = 1

    def makeLadders(self): # Ladder = 2
        for i in range(1, (self._height // (15 * 5) - 1)):
            ladderPos = math.floor(random.random() * (self._width / 30))
            ladderPos = int(10 + ladderPos)
            for k in range(0, 5):
                self.map[i * 5 + k][ladderPos] = self.map[i * 5 + k][32 - ladderPos] = 2

    def makePlayer(self): # Player = 3
        self.map[34][1] = self.map[33][1] = 3

    def drawImages(self):
        self.playerDrawn = 0
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 1:
                    wallLabel = QLabel()
                    pix = QPixmap('wood_block.png')
                    pixx = pix.scaled(QSize(self.image_size, self.image_size))
                    wallLabel.setPixmap(pixx)
                    wallLabel.move(y * 15 + 15 / 2, x * 15 + 15 / 2)
                    self.hbox.addWidget(wallLabel, x * 15 + 15 / 2, y * 15 + 15 / 2)

                if self.map[x][y] == 2:
                    ladderLabel = QLabel()
                    pix = QPixmap('ladder.png')
                    pixx = pix.scaled(QSize(self.image_size, self.image_size))
                    ladderLabel.setPixmap(pixx)
                    ladderLabel.move(y * 15 + 15 / 2, x * 15 + 15 / 2)
                    self.hbox.addWidget(ladderLabel, x * 15 + 15 / 2, y * 15 + 15 / 2)

                if self.map[x][y] == 3:
                    if self.playerDrawn == 0:
                        self.playerDrawn = 1
                    else:
                        playerLabel = QLabel()
                        pix = QPixmap('ItsAMeRight.png')
                        pixx = pix.scaled(QSize(self.image_size, self.image_size))
                        playerLabel.setPixmap(pixx)
                        playerLabel.move(y * 15 + 15 / 2, x * 15 + 15 / 2)
                        self.hbox.addWidget(playerLabel, x * 15 + 15 / 2, y * 15 + 15 / 2)

    # def clearScreen(self):
    # Clear previous screen

    def initializeBoard(self):
        # self.clearScreen()
        self.makeMap()
        self.makeWalls()
        self.makeLadders()
        self.makePlayer()
        self.drawImages()

    def initUI(self):
        self.startButton = QPushButton("New Game", self)
        self.startButton.resize(100, 32)
        self.startButton.move(100, 500)
        self.startButton.clicked.connect(self.on_start)

        self.map = []
        self._height = 600
        self._width = 500
        self.image_size = 18

        oImage = QImage("dk1.png")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.hbox = QGridLayout()
        self.hbox.setHorizontalSpacing(0)
        self.hbox.setVerticalSpacing(0)
        self.hbox.setColumnStretch(1, 4)
        self.hbox.setRowStretch(1, 4)

        self.hbox.addWidget(self.startButton)
        self.setLayout(self.hbox)

        self.setGeometry(400, 35, 600, 700)
        self.show()

    def on_start(self):
        oImage = QImage("Background.png")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.startButton.hide()

        self.initializeBoard()
        self.PrincessWidget = QWidget()
        self.MarioWidget = QWidget()

        #self.PrincessWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.hbox.addWidget(self.PrincessWidget, 1, 1)
        #self.MarioWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        #self.hbox.addWidget(self.MarioWidget, 34 * 15 + 15 / 2, 1 * 15 + 15 / 2)

        self.mover = Mover(self.MarioWidget)
        self.princess = Princess(self.PrincessWidget)
        self.mover.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
