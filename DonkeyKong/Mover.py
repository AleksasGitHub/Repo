import math
import random

from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, QtGui
from Lives import Lives
import sys
import time
from tkinter import *
import threading
from threading import Thread
from multiprocessing import Process, Pipe


class Mover(QLabel):
    def __init__(self, pipe: Pipe, livesWidget, levelLabel, donkeyKong, scoreLabel, my_obj_rwlock, leftPlayer, powerUp, powerUpWidget, parent=None):
        super().__init__(parent)
        self.left = leftPlayer
        if self.left:
            pix = QPixmap('Images/ItsAMeRight.png')
            self.playerValue = 3
            self.otherPlayerValue = 4
            self.setGeometry(-8, 621, 50, 70)
        else:
            pix = QPixmap('Images/ItsAMeLeft.png')
            self.playerValue = 4
            self.otherPlayerValue = 3
            self.setGeometry(533, 621, 50, 70)

        pixx = pix.scaled(QSize(50, 70))
        self.setPixmap(pixx)
        self.powerUpWidget = powerUpWidget
        self.powerUp = powerUp
        self.pipe = pipe
        self.PlayerX = 0
        self.PlayerY = 0
        self.lives = 3
        self.platformsList = []
        self.donkey = donkeyKong
        self.scoreLabel = scoreLabel
        self.score = 0
        self.my_obj_rwlock = my_obj_rwlock
        self.lW = livesWidget
        self.levelLabel = levelLabel
        self.th = Thread(target=self.check_lives, args=(livesWidget, self.donkey,))
        self.th1 = Thread(target=self.check_level, args=(levelLabel, livesWidget, self.donkey,))
        self.th2 = Thread(target=self.checkPowerUp, args=(livesWidget,))
        self.th.start()
        self.th1.start()
        self.th2.start()

    def check_lives(self, livesWidget, donkey):
        while True:
            self.getPosition()
            with self.my_obj_rwlock.w_locked():
                self.pipe.send("getCharacter %d %d" % (self.PlayerX, self.PlayerY))
                character1 = int(self.pipe.recv())
                self.pipe.send("getCharacter %d %d" % (self.PlayerX - 1, self.PlayerY))
                character2 = int(self.pipe.recv())
            b = (self.playerValue + 16 <= character2 <= 39 + self.playerValue and character2 != 24 + self.playerValue) or (self.playerValue + 16 <= character1 <= 39 + self.playerValue and character1 != 24 + self.playerValue)
            if b:
                if self.left:
                    pix = QPixmap('Images/ItsAMeRight.png')
                    self.setGeometry(-8, 621, 50, 70)
                else:
                    pix = QPixmap('Images/ItsAMeLeft.png')
                    self.setGeometry(533, 621, 50, 70)
                pixx = pix.scaled(QSize(50, 70))
                self.setPixmap(pixx)
                with self.my_obj_rwlock.w_locked():
                    if self.left:
                        self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY, -self.playerValue))
                        self.pipe.send("write %d %d %d" % (self.PlayerX - 1, self.PlayerY, -self.playerValue))
                        self.pipe.send("write 33 1 %d" % self.playerValue)
                        self.pipe.send("write 34 1 %d" % self.playerValue)
                    else:
                        self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY, -self.playerValue))
                        self.pipe.send("write %d %d %d" % (self.PlayerX - 1, self.PlayerY, -self.playerValue))
                        self.pipe.send("write 33 31 %d" % self.playerValue)
                        self.pipe.send("write 34 31 %d" % self.playerValue)
                if self.lives - 1 > 0:
                    self.lives = self.lives-1
                    livesWidget.lose_life(self.lives)
                #else game over
                self.platformsList = []
            time.sleep(0.5)

    def check_level(self, levelLabel, livesWidget, donkey):
        while True:
            self.getPosition()
            with self.my_obj_rwlock.w_locked():
                self.pipe.send("getCharacter %d %d" % (self.PlayerX, self.PlayerY))
                character1 = int(self.pipe.recv())
                self.pipe.send("getCharacter %d %d" % (self.PlayerX - 1, self.PlayerY))
                character2 = int(self.pipe.recv())
            #if self.map[self.PlayerX][self.PlayerY - 1] == 27 or self.map[self.PlayerX - 1][self.PlayerY+1] == 27 or self.map[self.PlayerX - 1][self.PlayerY -1] == 27 or self.map[self.PlayerX - 1][self.PlayerY-1] == 27:
            b = character1 == 24 + self.playerValue
            if b:
                if self.left:
                    pix = QPixmap('Images/ItsAMeRight.png')
                    self.setGeometry(-8, 621, 50, 70)
                else:
                    pix = QPixmap('Images/ItsAMeLeft.png')
                    self.setGeometry(533, 621, 50, 70)
                pixx = pix.scaled(QSize(50, 70))
                self.setPixmap(pixx)
                self.PlayerX = 0
                self.PlayerY = 0
                with self.my_obj_rwlock.w_locked():
                    self.pipe.send("restartMap")
                donkey.setGeometry(262, 112, 70, 80)
                levelLabel.level_up()
                self.lives = 3
                livesWidget.lose_life(self.lives)
                self.score = self.score + 5
                self.scoreLabel.change_score(self.score)
                self.platformsList = []
            time.sleep(0.5)

    def checkPowerUp(self, livesWidget):
        while True:
            self.getPosition()
            with self.my_obj_rwlock.w_locked():
                self.pipe.send("getCharacter %d %d" % (self.PlayerX, self.PlayerY))
                character1 = int(self.pipe.recv())
                self.pipe.send("getCharacter %d %d" % (self.PlayerX - 1, self.PlayerY))
                character2 = int(self.pipe.recv())
            b = (character1 == 8 + self.playerValue or character1 == 10 + self.playerValue or character1 == 8 + self.playerValue + self.otherPlayerValue or character1 == 10 + self.playerValue + self.otherPlayerValue) or \
                (character2 == 8 + self.playerValue or character2 == 10 + self.playerValue or character2 == 8 + self.playerValue + self.otherPlayerValue or character2 == 10 + self.playerValue + self.otherPlayerValue)
            if b:
                i = random.randrange(0, 101, 1) % 2
                if i == 0:
                    if self.lives - 1 > 0:
                        self.lives = self.lives - 1
                        livesWidget.lose_life(self.lives)
                    # else game over
                else:
                    if self.lives + 1 <= 3:
                        self.lives = self.lives + 1
                        livesWidget.lose_life(self.lives)
                self.powerUp.hide()
                del self.powerUp
                with self.my_obj_rwlock.w_locked():
                    self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY, -8))
            time.sleep(0.5)

    def getPowerUpPosition(self):
        with self.my_obj_rwlock.w_locked():
            self.pipe.send('readCoordinates PowerUp')
            s = self.pipe.recv()
            char = s.split()
            self.PowerUpX = int(char[0])
            self.PowerUpY = int(char[1])

    def getPosition(self):
        with self.my_obj_rwlock.w_locked():
            if self.left:
                self.pipe.send('readCoordinates Player1')
            else:
                self.pipe.send('readCoordinates Player2')
            s = self.pipe.recv()
            char = s.split()
            self.PlayerX = int(char[0])
            self.PlayerY = int(char[1])

    def check_score(self, previousX, newX):
        if previousX == 5 or previousX == 10 or previousX == 15 or previousX == 20 or previousX == 25 or previousX == 30:
            if not(newX == 5 or newX == 10 or newX == 15 or newX == 20 or newX == 25 or newX == 30):
                if previousX not in self.platformsList:
                  self.platformsList.append(previousX)
                  self.score = self.score + 1
                  self.scoreLabel.change_score(self.score)

    def keyPressEvent(self, event):

        if self.left:
            up = Qt.Key_Up
            down = Qt.Key_Down
            left = Qt.Key_Left
            right = Qt.Key_Right
        else:
            up = Qt.Key_W
            down = Qt.Key_S
            left = Qt.Key_A
            right = Qt.Key_D

        self.getPosition()
        if event.key() == up:
            with self.my_obj_rwlock.w_locked():
                self.pipe.send("getCharacter %d %d" % (self.PlayerX , self.PlayerY))
                character = int(self.pipe.recv())
                b = character == 2 + self.playerValue or character == 2 + self.playerValue + self.otherPlayerValue or character == 10 + self.playerValue + self.otherPlayerValue
            if b:
                self.move(self.x(), self.y() - 19)
                self.previousX = self.PlayerX
                with self.my_obj_rwlock.w_locked():
                    self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY, -self.playerValue))
                    self.pipe.send("write %d %d %d" % (self.PlayerX - 2, self.PlayerY, self.playerValue))
                self.getPosition()
                self.newX = self.PlayerX
                self.check_score(self.previousX, self.newX)

        elif event.key() == down:
            with self.my_obj_rwlock.w_locked():
                self.pipe.send("printMap")
            with self.my_obj_rwlock.w_locked():
                self.pipe.send("getCharacter %d %d" % (self.PlayerX + 1, self.PlayerY))
                character = int(self.pipe.recv())
                b = character == 2 or character == 2 + self.otherPlayerValue or character == 10 + self.otherPlayerValue
            if b:
            #if self.y() + 19 <= 630:
               #if self.map[self.PlayerX+1][self.PlayerY] == 5 or self.map[self.PlayerX + 1][self.PlayerY] == 2:
                self.move(self.x(), self.y() + 19)
                with self.my_obj_rwlock.w_locked():
                    self.pipe.send("write %d %d %d" % (self.PlayerX + 1, self.PlayerY, self.playerValue))
                    self.pipe.send("write %d %d %d" % (self.PlayerX - 1, self.PlayerY, -self.playerValue))

        elif event.key() == left:
            with self.my_obj_rwlock.w_locked():
                self.pipe.send("getCharacter %d %d" % (self.PlayerX, self.PlayerY - 1))
                character = int(self.pipe.recv())
                b1 = character != 1
            if b1:
                with self.my_obj_rwlock.w_locked():
                    self.pipe.send("getCharacter %d %d" % (self.PlayerX, self.PlayerY))
                    character1 = int(self.pipe.recv())
                    self.pipe.send("getCharacter %d %d" % (self.PlayerX + 1, self.PlayerY))
                    character2 = int(self.pipe.recv())
                    b2 = ((character2 == 2 and character1 == 2 + self.playerValue) or (character2 == 2 + self.otherPlayerValue and character1 == 2 + self.playerValue) or (character2 == 10 and character1 == 2 + self.playerValue) or (character2 == 10 + self.otherPlayerValue and character1 == 2 + self.playerValue))
                if not b2:
                    self.move(self.x() - 18, self.y())
                    pix = QPixmap('Images/ItsAMeLeft.png')
                    pixx = pix.scaled(QSize(50, 70))
                    self.setPixmap(pixx)
                    with self.my_obj_rwlock.w_locked():
                        self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY, -self.playerValue))
                        self.pipe.send("write %d %d %d" % (self.PlayerX-1, self.PlayerY, -self.playerValue))
                        self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY-1, self.playerValue))
                        self.pipe.send("write %d %d %d" % (self.PlayerX-1, self.PlayerY-1, self.playerValue))
        elif event.key() == right:
            with self.my_obj_rwlock.w_locked():
                self.pipe.send("getCharacter %d %d" % (self.PlayerX, self.PlayerY + 1))
                character = self.pipe.recv()
                b1 = character != 1
            if b1:
                with self.my_obj_rwlock.w_locked():
                    self.pipe.send("getCharacter %d %d" % (self.PlayerX, self.PlayerY))
                    character1 = int(self.pipe.recv())
                    self.pipe.send("getCharacter %d %d" % (self.PlayerX + 1, self.PlayerY))
                    character2 = int(self.pipe.recv())
                    b2 = ((character2 == 2 and character1 == 2 + self.playerValue) or (
                                character2 == 2 + self.otherPlayerValue and character1 == 2 + self.playerValue) or (
                                      character2 == 10 and character1 == 2 + self.playerValue) or (
                                      character2 == 10 + self.otherPlayerValue and character1 == 2 + self.playerValue))
                if not b2:
                    self.move(self.x() + 18, self.y())
                    pix = QPixmap('Images/ItsAMeRight.png')
                    pixx = pix.scaled(QSize(50, 70))
                    self.setPixmap(pixx)
                    with self.my_obj_rwlock.w_locked():
                        self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY, -self.playerValue))
                        self.pipe.send("write %d %d %d" % (self.PlayerX - 1, self.PlayerY, -self.playerValue))
                        self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY + 1, self.playerValue))
                        self.pipe.send("write %d %d %d" % (self.PlayerX - 1, self.PlayerY + 1, self.playerValue))
        else:
            QLabel.keyPressEvent(self, event)
