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


class Mover(QLabel):
    def __init__(self, map, livesWidget, levelLabel, donkeyKong, scoreLabel, my_obj_rwlock, leftPlayer, parent=None):
        super().__init__(parent)
        self.left = leftPlayer
        if self.left:
            pix = QPixmap('Images/ItsAMeRight.png')
            self.playerValue = 3
            self.otherPlayerValue = 4
            self.setGeometry(-8, 621, 50, 70)
            self.lives=3
        else:
            pix = QPixmap('Images/ItsAMeLeft.png')
            self.playerValue = 4
            self.otherPlayerValue = 3
            self.setGeometry(533, 621, 50, 70)
            self.lives=0

        pixx = pix.scaled(QSize(50, 70))
        self.setPixmap(pixx)
        self.map = map
        self.PlayerX = 0
        self.PlayerY = 0
        #self.lives = 3
        self.platformsList = []
        self.donkey = donkeyKong
        self.scoreLabel = scoreLabel
        self.score = 0
        self.my_obj_rwlock = my_obj_rwlock
        self.th = Thread(target=self.check_lives, args=(livesWidget, self.donkey,))
        self.th1 = Thread(target=self.check_level, args=(levelLabel, livesWidget, self.donkey,))
        self.th.start()
        self.th1.start()

    def check_lives(self, livesWidget, donkey):
        while True:
            self.getPosition()
            #if self.map[self.PlayerX][self.PlayerY] >= 9 or self.map[self.PlayerX - 1][self.PlayerY] >= 9:
            with self.my_obj_rwlock.r_locked():
                b = self.playerValue + 16 <= self.map[self.PlayerX - 1][self.PlayerY] <= 39 + self.playerValue and self.map[self.PlayerX - 1][self.PlayerY] != 24 + self.playerValue
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
                    donkey.map = self.map
                donkey.setGeometry(262, 112, 70, 80)

                if self.lives - 1 > 0:
                    self.lives = self.lives-1
                    livesWidget.lose_life(self.lives)
                #else game over
                self.platformsList = []
            time.sleep(0.5)

    def check_level(self, levelLabel, livesWidget, donkey):
        while True:
            self.getPosition()
            #if self.map[self.PlayerX][self.PlayerY - 1] == 27 or self.map[self.PlayerX - 1][self.PlayerY+1] == 27 or self.map[self.PlayerX - 1][self.PlayerY -1] == 27 or self.map[self.PlayerX - 1][self.PlayerY-1] == 27:
            with self.my_obj_rwlock.r_locked():
                b = self.map[self.PlayerX][self.PlayerY] == 24 + self.playerValue
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
                    donkey.map = self.map
                donkey.setGeometry(262, 112, 70, 80)
                levelLabel.level_up()
                self.lives = 3
                livesWidget.lose_life(self.lives)
                self.score = self.score + 5
                self.scoreLabel.change_score(self.score)
                self.platformsList = []
            time.sleep(0.5)

    def getPosition(self):
            self.playerDrawn = 0
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    with self.my_obj_rwlock.r_locked():
                        if self.map[x][y] == self.playerValue or self.map[x][y] == self.playerValue + 2 or self.map[x][y] == self.playerValue + self.otherPlayerValue or self.map[x][y] == self.playerValue + self.otherPlayerValue + 2 or self.map[x][y] == 16 + self.playerValue or self.map[x][y] == self.playerValue + self.otherPlayerValue + 16 or self.map[x][y] == 8 + self.playerValue or self.map[x][y] == 31 + self.playerValue or self.map[x][y] == 24 + self.playerValue:
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
                with self.my_obj_rwlock.r_locked():
                    row.append(self.map[x][y])
            print(row)

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
            with self.my_obj_rwlock.r_locked():
                b = self.map[self.PlayerX][self.PlayerY] == 2 + self.playerValue or self.map[self.PlayerX][self.PlayerY] == 2 + self.playerValue + self.otherPlayerValue or self.map[self.PlayerX][self.PlayerY] == 10 + self.playerValue + self.otherPlayerValue
            if b:
                self.move(self.x(), self.y() - 19)
                self.previousX = self.PlayerX
                with self.my_obj_rwlock.w_locked():
                    self.map[self.PlayerX][self.PlayerY] = self.map[self.PlayerX][self.PlayerY] - self.playerValue
                    self.map[self.PlayerX - 2][self.PlayerY] = self.map[self.PlayerX - 2][self.PlayerY] + self.playerValue
                self.getPosition()
                self.newX = self.PlayerX
                self.check_score(self.previousX, self.newX)
        elif event.key() == down:
            #self.printMap()
            with self.my_obj_rwlock.r_locked():
                b = self.map[self.PlayerX + 1][self.PlayerY] == 2 or self.map[self.PlayerX + 1][self.PlayerY] == 2 + self.otherPlayerValue or self.map[self.PlayerX + 1][self.PlayerY] == 10 + self.otherPlayerValue
            if b:
            #if self.y() + 19 <= 630:
               #if self.map[self.PlayerX+1][self.PlayerY] == 5 or self.map[self.PlayerX + 1][self.PlayerY] == 2:
                self.move(self.x(), self.y() + 19)
                with self.my_obj_rwlock.w_locked():
                    self.map[self.PlayerX + 1][self.PlayerY] = self.map[self.PlayerX + 1][self.PlayerY] + self.playerValue
                    self.map[self.PlayerX - 1][self.PlayerY] = self.map[self.PlayerX - 1][self.PlayerY] - self.playerValue


        elif event.key() == left:
            with self.my_obj_rwlock.r_locked():
                b1 = self.map[self.PlayerX][self.PlayerY - 1] != 1
            if b1:
                with self.my_obj_rwlock.r_locked():
                    b2 = ((self.map[self.PlayerX + 1][self.PlayerY] == 2 and self.map[self.PlayerX][self.PlayerY] == 2 + self.playerValue) or (self.map[self.PlayerX + 1][self.PlayerY] == 2 + self.otherPlayerValue and self.map[self.PlayerX][self.PlayerY] == 2 + self.playerValue) or (self.map[self.PlayerX + 1][self.PlayerY] == 10 and self.map[self.PlayerX][self.PlayerY] == 2 + self.playerValue) or (self.map[self.PlayerX + 1][self.PlayerY] == 10 + self.otherPlayerValue and self.map[self.PlayerX][self.PlayerY] == 2 + self.playerValue))
                if not b2:
                    self.move(self.x() - 18, self.y())
                    pix = QPixmap('Images/ItsAMeLeft.png')
                    pixx = pix.scaled(QSize(50, 70))
                    self.setPixmap(pixx)
                    with self.my_obj_rwlock.w_locked():
                        self.map[self.PlayerX][self.PlayerY] = self.map[self.PlayerX][self.PlayerY] - self.playerValue
                        self.map[self.PlayerX-1][self.PlayerY] = self.map[self.PlayerX-1][self.PlayerY] - self.playerValue
                        self.map[self.PlayerX][self.PlayerY-1] = self.map[self.PlayerX][self.PlayerY-1] + self.playerValue
                        self.map[self.PlayerX-1][self.PlayerY-1] = self.map[self.PlayerX-1][self.PlayerY-1] + self.playerValue

                   # self.printMap()
        elif event.key() == right:
            with self.my_obj_rwlock.r_locked():
                b1 = self.map[self.PlayerX][self.PlayerY + 1] != 1
            if b1:
            #if self.x() + 18 <= 532:
                with self.my_obj_rwlock.r_locked():
                    b2 = ((self.map[self.PlayerX + 1][self.PlayerY] == 2 and self.map[self.PlayerX][self.PlayerY] == 2 + self.playerValue) or (self.map[self.PlayerX + 1][self.PlayerY] == 2 + self.otherPlayerValue and self.map[self.PlayerX][self.PlayerY] == 2 + self.playerValue) or (self.map[self.PlayerX + 1][self.PlayerY] == 10 and self.map[self.PlayerX][self.PlayerY] == 2 + self.playerValue) or (self.map[self.PlayerX + 1][self.PlayerY] == 10 + self.otherPlayerValue and self.map[self.PlayerX][self.PlayerY] == 2 + self.playerValue))
                if not b2:
                    self.move(self.x() + 18, self.y())
                    pix = QPixmap('Images/ItsAMeRight.png')
                    pixx = pix.scaled(QSize(50, 70))
                    self.setPixmap(pixx)
                    with self.my_obj_rwlock.w_locked():
                        self.map[self.PlayerX][self.PlayerY] = self.map[self.PlayerX][self.PlayerY] - self.playerValue
                        self.map[self.PlayerX-1][self.PlayerY] = self.map[self.PlayerX-1][self.PlayerY] - self.playerValue
                        self.map[self.PlayerX][self.PlayerY+1] = self.map[self.PlayerX][self.PlayerY+1] + self.playerValue
                        self.map[self.PlayerX-1][self.PlayerY+1] = self.map[self.PlayerX-1][self.PlayerY+1] + self.playerValue

                    #self.printMap()
        else:
            QLabel.keyPressEvent(self, event)
