import math
import random

from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, QtGui
from Mover import Mover
from DonkeyKong import DonkeyKong
from Princess import Princess
from Lives import Lives
from Score import Score
from Level import Level
from PowerUp import PowerUp
import sys
import time
from tkinter import *
import threading
from threading import Thread
from RWLock import RWLock


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('Images/doKo.png'))
        self.setWindowTitle("Donkey Kong")
        self.initUI(True)

    def printMap(self):
        for x in range(len(self.map)):
            row = []
            for y in range(len(self.map[x])):
                with self.my_obj_rwlock.r_locked():
                    row.append(self.map[x][y])
            print(row)

    def initUI(self,firstTime):
        if (not firstTime):
            self.ScoreLabelText.hide()
            self.ScoreLabelText2.hide()
            self.menuButton.hide()
            self.scoreLabelMover1.hide()
            self.scoreLabelMover2.hide()
            self.scoreLabelResult.hide()
        self.startButton = QPushButton("New Game", self)
        self.startButton.resize(100, 32)
        self.startButton.setGeometry(130, 600, 100, 32)
        self.startButton.setStyleSheet("background-color: green; color: white; font-size:14px; font: bold System")
        self.startButton.clicked.connect(self.on_start)

        self.exitButton = QPushButton("Exit", self)
        self.exitButton.resize(100, 32)
        self.exitButton.setGeometry(360, 600, 100, 32)
        self.exitButton.setStyleSheet("background-color: red; color: white; font-size:14px; font: bold System")
        self.exitButton.clicked.connect(self.exit_game)

        self.map = \
            [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 24, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 24, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 24, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
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
             [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
             [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self._height = 600
        self._width = 500
        self.image_size = 18

        oImage = QImage("Images/dk1.png")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.hbox = QGridLayout()
        # self.hbox.setHorizontalSpacing(0)
        # self.hbox.setVerticalSpacing(0)
        self.hbox.setColumnStretch(1, 6)
        self.hbox.setRowStretch(1, 6)

        self.startButton.show()
        self.exitButton.show()
        self.setLayout(self.hbox)

        self.setGeometry(400, 35, 600, 700)
        self.show()

    def exit_game(self):
        self.close()

    def on_start(self):
        oImage = QImage("Images/Background2.png")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.startButton.hide()
        self.exitButton.hide()

        self.my_obj_rwlock = RWLock()

        self.PrincessWidget = QWidget()
        self.MarioWidget = QWidget()
        self.DonkeyWidget = QWidget()
        self.LivesWidget1 = QWidget()
        self.ScoreLabel1 = QLabel("Score: 0", self)
        self.LivesWidget2 = QWidget()
        self.ScoreLabel2 = QLabel("Score: 0", self)
        self.LevelLabel = QLabel("Level ", self)
        self.PowerUpWidget = QWidget()

        self.hbox.addWidget(self.ScoreLabel1, 1, 1)
        self.hbox.addWidget(self.ScoreLabel2, 1, 1)
        self.hbox.addWidget(self.LevelLabel, 1, 1)
        self.hbox.addWidget(self.PrincessWidget, 1, 1)
        self.hbox.addWidget(self.MarioWidget, 1, 1)
        self.hbox.addWidget(self.DonkeyWidget, 1, 1)
        self.hbox.addWidget(self.LivesWidget1, 1, 1)
        self.hbox.addWidget(self.LivesWidget2, 1, 1)
        self.hbox.addWidget(self.PowerUpWidget, 1, 1)

        self.x = random.randrange(0, 4)
        self.y = random.randrange(0, 31)
        self.map[self.x * 5 + 14][self.y + 1] = self.map[self.x * 5 + 14][self.y + 1] + 8

        self.powerUp = PowerUp(self.x, self.y, self.PowerUpWidget)
        self.scoreLabel1 = Score(self.ScoreLabel1)
        self.scoreLabel2 = Score(self.ScoreLabel2)
        self.scoreLabel1.setGeometry(19, 48, 100, 38)
        self.scoreLabel2.setGeometry(450, 48, 100, 38)
        self.levelLabel = Level(self.LevelLabel)
        self.livesWidget1 = Lives(self.LivesWidget1)
        self.livesWidget2 = Lives(self.LivesWidget2)
        self.livesWidget1.setGeometry(9, 4, 100, 70)
        self.livesWidget2.setGeometry(440, 4, 100, 70)
        self.donkey = DonkeyKong(self.map, self.hbox, self.my_obj_rwlock, self.DonkeyWidget)
        self.mover1 = Mover(self.map, self.livesWidget1, self.levelLabel, self.donkey, self.scoreLabel1, self.my_obj_rwlock, True, self.powerUp, self.MarioWidget)
        self.mover2 = Mover(self.map, self.livesWidget2, self.levelLabel, self.donkey, self.scoreLabel2, self.my_obj_rwlock, False, self.powerUp, self.MarioWidget)
        self.princess = Princess(self.PrincessWidget)

        self.th = Thread(target=self.check_for_game_end)
        self.th.do_run = True
        self.th.start()

        self.mover1.setFocus()
        self.hbox.update()

    def printMap(self):
        while True:
            for x in range(len(self.map)):
                row = []
                for y in range(len(self.map[x])):
                    row.append(self.map[x][y])
                print(row)
            time.sleep(5)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
         for i in reversed(range(self.hbox.count())):
           widgetToRemove = self.hbox.itemAt(i).widget()
           self.hbox.removeWidget(widgetToRemove)
           widgetToRemove.setParent(None)

         self.princess.kill = True
         self.donkey.kill = True
         self.powerUp.kill = True
         self.resultInfo()

    def check_for_game_end(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
           if(self.mover1.lives==0 and self.mover2.lives==0):
               print("over")
               t.do_run = False
               #for i in reversed(range(self.hbox.count())):
                #  self.hbox.itemAt(i).widget().setParent(None)
               for i in reversed(range(self.hbox.count())):
                   widgetToRemove = self.hbox.itemAt(i).widget()
                   self.hbox.removeWidget(widgetToRemove)
                   widgetToRemove.setParent(None)
               self.princess.kill = True
               self.donkey.kill = True
               self.powerUp.kill = True
               self.resultInfo()
               #self.hbox.update()

           time.sleep(0.5)

    def resultInfo(self):
        oImage = QImage("Images/black.jpg")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        print("proba")

        self.setPalette(palette)
        self.menuButton = QPushButton("Menu", self)
        #self.hbox.addWidget(self.menuButton)
        self.menuButton.show()
        self.menuButton.resize(100, 32)
        self.menuButton.setGeometry(230, 500, 100, 32)
        self.menuButton.setStyleSheet("background-color: green; color: white; font-size:14px; font: bold System")
        self.menuButton.clicked.connect(lambda : self.initUI(False))


        self.ScoreLabelText = QLabel("Score: 0", self)
        self.hbox.addWidget(self.ScoreLabelText, 1, 1)
        self.scoreLabelText = Score(self.ScoreLabelText)
        self.scoreLabelText.setGeometry(70, 278, 100, 18)
        self.scoreLabelText.text(1)
        self.ScoreLabelText2 = QLabel("Score: 0", self)
        self.hbox.addWidget(self.ScoreLabelText2, 1, 1)
        self.scoreLabelText2 = Score(self.ScoreLabelText2)
        self.scoreLabelText2.setGeometry(370, 278, 100, 18)
        self.scoreLabelText2.text(2)

        self.ScoreLabelMover1 = QLabel("Score: 0", self)
        self.hbox.addWidget(self.ScoreLabelMover1, 1, 1)
        self.scoreLabelMover1 = Score(self.ScoreLabelMover1)
        self.scoreLabelMover1.setGeometry(120, 348, 100, 38)
        self.scoreLabelMover1.setText(format(str(self.mover1.score)))

        self.ScoreLabelMover2 = QLabel("Score: 0", self)
        self.hbox.addWidget(self.ScoreLabelMover2, 1, 1)
        self.scoreLabelMover2 = Score(self.ScoreLabelMover2)
        self.scoreLabelMover2.setGeometry(420, 348, 100, 38)
        self.scoreLabelMover2.setText(format(str(self.mover2.score)))

        self.ScoreLabelResult = QLabel("Score: 0", self)
        self.hbox.addWidget(self.ScoreLabelResult, 1, 1)
        self.scoreLabelResult = Score(self.ScoreLabelResult)
        self.scoreLabelResult.setGeometry(210, 148, 300, 38)
        self.scoreLabelResult.setStyleSheet("background-color: black; color: red; font-size:18px; font: bold System")
        if(self.mover1.score>self.mover2.score):
            self.scoreLabelResult.setText("PLAYER 1 WON")
        elif(self.mover1.score<self.mover2.score):
            self.scoreLabelResult.setText("PLAYER 2 WON")
        else:
            self.scoreLabelResult.setText("NO WINNER")

        self.hbox.update()
        self.setGeometry(400, 35, 600, 700)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
