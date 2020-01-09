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
    def __init__(self,next_level, pipe: Pipe, self_pipe: Pipe, power_up_pipe: Pipe, donkey_pipe: Pipe, movement_pipe: Pipe, livesWidget, levelLabel, scoreLabel, my_obj_rwlock, leftPlayer, powerUp, powerUpWidget, parent=None):
        super().__init__(parent)
        self.left = leftPlayer
        self.self_pipe = self_pipe
        self.power_up_pipe = power_up_pipe
        self.donkey_pipe = donkey_pipe
        self.movement_pipe = movement_pipe
        self.next_level = next_level
        self.kill = False
        if self.left:
            pix = QPixmap('Images/ItsAMeRight.png')
            self.playerValue = 3
            self.otherPlayerValue = 4
            self.setGeometry(-8, 621, 50, 70)
        else:
            pix = QPixmap('Images/LuiguiLeft.png')
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
        self.scoreLabel = scoreLabel
        self.score = 0
        self.my_obj_rwlock = my_obj_rwlock
        self.lW = livesWidget
        self.levelLabel = levelLabel
        self.th = Thread(target=self.check_lives, args=(livesWidget,))
        self.th1 = Thread(target=self.check_level, args=(levelLabel, livesWidget,))
        self.th2 = Thread(target=self.checkPowerUp, args=(livesWidget,))
        self.restart_thread = Thread(target=self.restart, args=(livesWidget,))
        self.movement_thread = Thread(target=self.movePlayer, args=[])
        self.th.start()
        self.th1.start()
        self.th2.start()
        self.restart_thread.start()
        self.movement_thread.start()

    def restart(self, livesWidget):
        while not self.kill:
            self.self_pipe.recv()
            if self.left:
                pix = QPixmap('Images/ItsAMeRight.png')
                self.setGeometry(-8, 621, 50, 70)
            else:
                pix = QPixmap('Images/LuiguiLeft.png')
                self.setGeometry(533, 621, 50, 70)
            pixx = pix.scaled(QSize(50, 70))
            self.setPixmap(pixx)
            livesWidget.lose_life(3)

    def check_lives(self, livesWidget):
        while not self.kill:
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
                    pix = QPixmap('Images/LuiguiLeft.png')
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
                self.lives = self.lives - 1
                livesWidget.lose_life(self.lives)

                if self.lives == 0:
                  self.hide()
                #self.platformsList = []
                self.pipe.send('printMap')
            time.sleep(0.5)

    def check_level(self, levelLabel, livesWidget):
        while not self.kill:
            self.getPosition()
            with self.my_obj_rwlock.w_locked():
                self.pipe.send("getCharacter %d %d" % (self.PlayerX, self.PlayerY))
                character1 = int(self.pipe.recv())
                self.pipe.send("getCharacter %d %d" % (self.PlayerX - 1, self.PlayerY))
                character2 = int(self.pipe.recv())
            b = character1 == 24 + self.playerValue or character1 == 24 + self.playerValue + self.otherPlayerValue
            if b:
                with self.my_obj_rwlock.w_locked():
                    if self.left:
                        pix = QPixmap('Images/ItsAMeRight.png')
                        self.setGeometry(-8, 621, 50, 70)
                    else:
                        pix = QPixmap('Images/LuiguiLeft.png')
                        self.setGeometry(533, 621, 50, 70)
                    pixx = pix.scaled(QSize(50, 70))
                    self.setPixmap(pixx)
                    self.PlayerX = 0
                    self.PlayerY = 0

                    self.pipe.send("restartMap")
                    self.donkey_pipe.send("Restart")
                    self.self_pipe.send("Restart")
                    self.power_up_pipe.send("Restart")
                    levelLabel.level_up()
                    self.lives = 3
                    livesWidget.lose_life(self.lives)
                    self.score = self.score + 5
                    self.scoreLabel.change_score(self.score)
                    self.platformsList = []
                    self.next_level.animation()
                    self.pipe.send('printMap')
            time.sleep(0.5)

    def checkPowerUp(self, livesWidget):
        while not self.kill:
            self.getPosition()
            with self.my_obj_rwlock.w_locked():
                self.pipe.send("getCharacter %d %d" % (self.PlayerX, self.PlayerY))
                character1 = int(self.pipe.recv())
                self.pipe.send("getCharacter %d %d" % (self.PlayerX - 1, self.PlayerY))
                character2 = int(self.pipe.recv())
            b1 = character1 == 8 + self.playerValue or character1 == 10 + self.playerValue or character1 == 8 + self.playerValue + self.otherPlayerValue or character1 == 10 + self.playerValue + self.otherPlayerValue
            b2 = character2 == 8 + self.playerValue or character2 == 10 + self.playerValue or character2 == 8 + self.playerValue + self.otherPlayerValue or character2 == 10 + self.playerValue + self.otherPlayerValue
            if b1 or b2:
                i = random.randrange(0, 101, 1) % 2
                if i == 0:
                    if self.lives - 1 > 0:
                        self.lives = self.lives - 1
                        livesWidget.lose_life(self.lives)
                    else:
                        self.lives = 0
                        livesWidget.lose_life(self.lives)
                        self.hide()
                else:
                    if self.lives + 1 <= 3:
                        self.lives = self.lives + 1
                        livesWidget.lose_life(self.lives)
                self.powerUp.hide()
                #del self.powerUp
                with self.my_obj_rwlock.w_locked():
                    if b1:
                        self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY, -8))
                    else:
                        self.pipe.send("write %d %d %d" % (self.PlayerX-1, self.PlayerY, -8))
                self.pipe.send('printMap')
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

    def movePlayer(self):
        while not self.kill:
            direction = self.movement_pipe.recv()
            '''if self.left:
                up = "W"
                down = Qt.Key_Down
                left = Qt.Key_Left
                right = Qt.Key_Right
            else:
                up = Qt.Key_W
                down = Qt.Key_S
                left = Qt.Key_A
                right = Qt.Key_D'''

            self.getPosition()
            if direction == "W" or direction == "I":
                with self.my_obj_rwlock.w_locked():
                    self.pipe.send("getCharacter %d %d" % (self.PlayerX , self.PlayerY))
                    character = int(self.pipe.recv())
                    b = character == 2 + self.playerValue or character == 2 + self.playerValue + self.otherPlayerValue or character == 10 + self.playerValue + self.otherPlayerValue
                if b:
                    if self.PlayerX > 31:
                        up = 19
                    elif self.PlayerX > 26:
                        up = 20
                    elif self.PlayerX > 21:
                        up = 19
                    elif self.PlayerX > 16:
                        up = 20
                    else:
                        up = 19
                    self.move(self.x(), self.y() - up)
                    self.previousX = self.PlayerX
                    with self.my_obj_rwlock.w_locked():
                        self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY, -self.playerValue))
                        self.pipe.send("write %d %d %d" % (self.PlayerX - 2, self.PlayerY, self.playerValue))
                    self.getPosition()
                    self.newX = self.PlayerX
                    self.check_score(self.previousX, self.newX)

            elif direction == "S" or direction == "K":
                with self.my_obj_rwlock.w_locked():
                    self.pipe.send("printMap")
                with self.my_obj_rwlock.w_locked():
                    self.pipe.send("getCharacter %d %d" % (self.PlayerX + 1, self.PlayerY))
                    character = int(self.pipe.recv())
                    b = character == 2 or character == 2 + self.otherPlayerValue or character == 10 + self.otherPlayerValue
                if b:
                #if self.y() + 19 <= 630:
                   #if self.map[self.PlayerX+1][self.PlayerY] == 5 or self.map[self.PlayerX + 1][self.PlayerY] == 2:
                    if self.PlayerX > 31:
                        down = 19
                    elif self.PlayerX > 26:
                        down = 20
                    elif self.PlayerX > 21:
                        down = 19
                    elif self.PlayerX > 16:
                        down = 20
                    else:
                        down = 19
                    self.move(self.x(), self.y() + down)
                    with self.my_obj_rwlock.w_locked():
                        self.pipe.send("write %d %d %d" % (self.PlayerX + 1, self.PlayerY, self.playerValue))
                        self.pipe.send("write %d %d %d" % (self.PlayerX - 1, self.PlayerY, -self.playerValue))

            elif direction == "A" or direction == "J":
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
                        if self.left:
                            pix = QPixmap('Images/ItsAMeLeft.png')
                        else:
                            pix = QPixmap('Images/LuiguiLeft.png')
                        pixx = pix.scaled(QSize(50, 70))
                        self.setPixmap(pixx)
                        with self.my_obj_rwlock.w_locked():
                            self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY, -self.playerValue))
                            self.pipe.send("write %d %d %d" % (self.PlayerX-1, self.PlayerY, -self.playerValue))
                            self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY-1, self.playerValue))
                            self.pipe.send("write %d %d %d" % (self.PlayerX-1, self.PlayerY-1, self.playerValue))
            elif direction == "D" or direction == "L":
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
                        if self.left:
                            pix = QPixmap('Images/ItsAMeRight.png')
                        else:
                            pix = QPixmap('Images/LuiguiRight.png')
                        pixx = pix.scaled(QSize(50, 70))
                        self.setPixmap(pixx)
                        with self.my_obj_rwlock.w_locked():
                            self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY, -self.playerValue))
                            self.pipe.send("write %d %d %d" % (self.PlayerX - 1, self.PlayerY, -self.playerValue))
                            self.pipe.send("write %d %d %d" % (self.PlayerX, self.PlayerY + 1, self.playerValue))
                            self.pipe.send("write %d %d %d" % (self.PlayerX - 1, self.PlayerY + 1, self.playerValue))
