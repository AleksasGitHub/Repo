import math
import random

from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt
import sys
import time
import threading
from threading import Thread


class DonkeyKong(QLabel):
    def __init__(self, map, parent=None):
        super().__init__(parent)
        self.setGeometry(262, 112, 70, 80)
        pix = QPixmap('doKo.png')
        pixx = pix.scaled(QSize(70, 80))
        self.setPixmap(pixx)
        self.th = Thread(target=self.moveRandom, args=())
        self.th.start()
        self.map = map
        self.DonkeyX = 0
        self.DonkeyY = 0

    def getPosition(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 3 or self.map[x][y] == 5:
                    if self.playerDrawn == 0:
                        self.playerDrawn = 1
                    else:
                        self.DonkeyX = x
                        self.DonkeyY = y
                        return

    def moveRandom(self):
        while True:
            i = 1
            #i = random.randrange(0, 101, 1) % 2
            if i == 0:
                for j in range (0, 3):
                    if self.x() - 18 >= 0:
                        self.move(self.x() - 18, self.y())
                        pix = QPixmap('doKo.png')
                        pixx = pix.scaled(QSize(70, 80))
                        self.setPixmap(pixx)
                        time.sleep(0.5)
            else:
                for j in range(0, 3):
                    if self.x() + 18 <= 510:
                        self.move(self.x() + 18, self.y())
                        pix = QPixmap('doKo.png')
                        pixx = pix.scaled(QSize(70, 80))
                        self.setPixmap(pixx)
                        time.sleep(0.5)
            #time.sleep(0.5)


class Princess(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(260, 20, 50, 70)
        pix = QPixmap('peach2.png')
        pixx = pix.scaled(QSize(50, 70))
        self.setPixmap(pixx)
        self.th = Thread(target=self.wave, args=())
        self.th.start()

    def wave(self):
        while True:
            pix = QPixmap('wave.png')
            pixx = pix.scaled(QSize(50, 70))
            self.setPixmap(pixx)
            time.sleep(0.5)
            pix2 = QPixmap('peach2.png')
            pixx2 = pix2.scaled(QSize(50, 70))
            self.setPixmap(pixx2)
            time.sleep(0.5)


class Mover(QLabel):
    def __init__(self, map, parent=None):
        super().__init__(parent)
        self.setGeometry(-8, 621, 50, 70)
        pix = QPixmap('ItsAMeRight.png')
        pixx = pix.scaled(QSize(50, 70))
        self.setPixmap(pixx)
        self.map = map
        self.PlayerX = 0
        self.PlayerY = 0

    def getPosition(self):
        self.playerDrawn = 0
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 3 or self.map[x][y] == 5:
                    if self.playerDrawn == 0:
                        self.playerDrawn = 1
                    else:
                        self.PlayerX = x
                        self.PlayerY = y
                        return

    def printMap(self):
        for x in range(len(self.map)):
            row = []
            for y in range(len(self.map[x])):
                row.append(self.map[x][y])
            print(row)

    def keyPressEvent(self, event):
        self.getPosition()
        if event.key() == Qt.Key_Up:
            if self.map[self.PlayerX][self.PlayerY] == 5:
                self.move(self.x(), self.y() - 19)
                self.map[self.PlayerX][self.PlayerY] = self.map[self.PlayerX][self.PlayerY] - 3
                self.map[self.PlayerX - 2][self.PlayerY] = self.map[self.PlayerX - 2][self.PlayerY] + 3
                self.printMap()
        elif event.key() == Qt.Key_Down:
            if self.y() + 19 <= 630:
                if self.map[self.PlayerX+1][self.PlayerY] == 5 or self.map[self.PlayerX + 1][self.PlayerY] == 2:
                    self.move(self.x(), self.y() + 19)
                    self.map[self.PlayerX + 1][self.PlayerY] = self.map[self.PlayerX + 1][self.PlayerY] + 3
                    self.map[self.PlayerX - 1][self.PlayerY] = self.map[self.PlayerX - 1][self.PlayerY] - 3
                    self.printMap()
        elif event.key() == Qt.Key_Left:
            if self.x() - 18 >= -8:
                if not (self.map[self.PlayerX+1][self.PlayerY] == 2 and self.map[self.PlayerX + 1][self.PlayerY+1] == 0):
                    self.move(self.x() - 18, self.y())
                    pix = QPixmap('ItsAMeLeft.png')
                    pixx = pix.scaled(QSize(50, 70))
                    self.setPixmap(pixx)
                    self.map[self.PlayerX][self.PlayerY] = self.map[self.PlayerX][self.PlayerY] - 3
                    self.map[self.PlayerX-1][self.PlayerY] = self.map[self.PlayerX-1][self.PlayerY] - 3
                    self.map[self.PlayerX][self.PlayerY-1] = self.map[self.PlayerX][self.PlayerY-1] + 3
                    self.map[self.PlayerX-1][self.PlayerY-1] = self.map[self.PlayerX-1][self.PlayerY-1] + 3
                    self.printMap()
        elif event.key() == Qt.Key_Right:
            if self.x() + 18 <= 532:
                if not (self.map[self.PlayerX + 1][self.PlayerY] == 2 and self.map[self.PlayerX + 1][self.PlayerY + 1] == 0):
                    self.move(self.x() + 18, self.y())
                    pix = QPixmap('ItsAMeRight.png')
                    pixx = pix.scaled(QSize(50, 70))
                    self.setPixmap(pixx)
                    self.map[self.PlayerX][self.PlayerY] = self.map[self.PlayerX][self.PlayerY] - 3
                    self.map[self.PlayerX-1][self.PlayerY] = self.map[self.PlayerX-1][self.PlayerY] - 3
                    self.map[self.PlayerX][self.PlayerY+1] = self.map[self.PlayerX][self.PlayerY+1] + 3
                    self.map[self.PlayerX-1][self.PlayerY+1] = self.map[self.PlayerX-1][self.PlayerY+1] + 3
                    self.printMap()
        else:
            QLabel.keyPressEvent(self, event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.startButton = QPushButton("New Game", self)
        self.startButton.resize(100, 32)
        self.startButton.move(100, 500)
        self.startButton.clicked.connect(self.on_start)

        self.map = \
            [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

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

        self.PrincessWidget = QWidget()
        self.MarioWidget = QWidget()
        self.DonkeyWidget = QWidget()

        # self.PrincessWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.hbox.addWidget(self.PrincessWidget, 1, 1)
        # self.MarioWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.hbox.addWidget(self.MarioWidget, 1, 1)
        # self.DonkeyWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.hbox.addWidget(self.DonkeyWidget, 1, 1)

        self.mover = Mover(self.map, self.MarioWidget)
        self.princess = Princess(self.PrincessWidget)
        self.donkey = DonkeyKong(self.map, self.DonkeyWidget)
        self.mover.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
