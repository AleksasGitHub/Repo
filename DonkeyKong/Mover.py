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
    def __init__(self, map, livesWidget, parent=None):
        super().__init__(parent)
        self.setGeometry(-8, 621, 50, 70)
        pix = QPixmap('ItsAMeRight.png')
        pixx = pix.scaled(QSize(50, 70))
        self.setPixmap(pixx)
        self.map = map
        self.PlayerX = 0
        self.PlayerY = 0
        self.lives = 3
        self.th = Thread(target=self.check_lives, args=(livesWidget,))
        self.th.start()

    def check_lives(self, livesWidget):
        while True:
            self.getPosition()
            if self.map[self.PlayerX][self.PlayerY] >= 9 or self.map[self.PlayerX - 1][self.PlayerY] >= 9:
                  self.printMap()
                  #self.map[self.PlayerX][self.PlayerY] = self.map[self.PlayerX][self.PlayerY] - 3
                  #self.map[self.PlayerX - 1][self.PlayerY] = self.map[self.PlayerX - 1][self.PlayerY] - 3
                  self.setGeometry(-8, 621, 50, 70)
                  pix = QPixmap('ItsAMeRight.png')
                  pixx = pix.scaled(QSize(50, 70))
                  self.setPixmap(pixx)
                  self.PlayerX = 0
                  self.PlayerY = 0
                  self.map = \
                      [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0]]
                  if self.lives - 1 > 0:
                      self.lives = self.lives-1
                      if self.lives == 2:
                          livesWidget.lose_life(self.lives)
                      elif self.lives == 1:
                          livesWidget.lose_life(self.lives)
                  self.getPosition()
            time.sleep(0.5)


    def getPosition(self):
        self.playerDrawn = 0
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 3 or self.map[x][y] == 5 or self.map[x][y] >= 9:
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

                #self.printMap()
        elif event.key() == Qt.Key_Down:
            self.printMap()
            print(self.PlayerY)
            print(self.PlayerX)
            if self.y() + 19 <= 630:
                if self.map[self.PlayerX+1][self.PlayerY] == 5 or self.map[self.PlayerX + 1][self.PlayerY] == 2:
                    self.move(self.x(), self.y() + 19)
                    self.map[self.PlayerX + 1][self.PlayerY] = self.map[self.PlayerX + 1][self.PlayerY] + 3
                    self.map[self.PlayerX - 1][self.PlayerY] = self.map[self.PlayerX - 1][self.PlayerY] - 3


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

                   # self.printMap()
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

                    #self.printMap()
        else:
            QLabel.keyPressEvent(self, event)

