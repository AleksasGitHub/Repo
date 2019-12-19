import math
import random

from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, QtGui
import sys
import time
from tkinter import *
import threading
from threading import Thread





class DonkeyKong(QLabel):
    def __init__(self, map, parent=None):
        super().__init__(parent)
        self.map = map
        self.DonkeyX = 0
        self.DonkeyY = 0
        self.setGeometry(262, 112, 70, 80)
        pix = QPixmap('doKo.png')
        pixx = pix.scaled(QSize(70, 80))
        self.setPixmap(pixx)
        self.th = Thread(target=self.moveRandom, args=())
        self.th.start()

    def getPosition(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 6 or self.map[x][y] == 8 or self.map[x][y] >= 9:
                        self.DonkeyX = x
                        self.DonkeyY = y
                        return

    def printMap(self):
        for x in range(len(self.map)):
            row = []
            for y in range(len(self.map[x])):
                row.append(self.map[x][y])
            print(row)

    def moveRandom(self):
        while True:
            i = random.randrange(0, 101, 1) % 2
            times = random.randrange(3, 5)
            if i == 0:
                for j in range(0, times):
                    if self.x() - 18 >= 0:
                        self.getPosition()
                        self.move(self.x() - 18, self.y())
                        pix = QPixmap('doKo.png')
                        pixx = pix.scaled(QSize(70, 80))
                        self.setPixmap(pixx)
                        for k in range(0, 4):
                            self.map[self.DonkeyX + k][self.DonkeyY - 1] = self.map[self.DonkeyX + k][self.DonkeyY - 1] + 6
                            self.map[self.DonkeyX + k][self.DonkeyY + 3] = self.map[self.DonkeyX + k][self.DonkeyY + 3] - 6
                        #self.printMap()
                        time.sleep(0.5)
            else:
                for j in range(0, times):
                    if self.x() + 18 <= 510:
                        self.getPosition()
                        self.move(self.x() + 18, self.y())
                        pix = QPixmap('doKo.png')
                        pixx = pix.scaled(QSize(70, 80))
                        self.setPixmap(pixx)
                        for k in range(0, 4):
                            self.map[self.DonkeyX + k][self.DonkeyY + 4] = self.map[self.DonkeyX + k][self.DonkeyY + 4] + 6
                            self.map[self.DonkeyX + k][self.DonkeyY] = self.map[self.DonkeyX + k][self.DonkeyY] - 6
                        #self.printMap()
                        time.sleep(0.5)
