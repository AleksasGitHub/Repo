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


class Barrel(QLabel):
    def __init__(self, map, donkeyX, donkeyY, parent = None):
        super().__init__(parent)
        self.map = map
        self.BarrelX = donkeyX + 2
        self.BarrelY = donkeyY + 1
        self.setGeometry((donkeyX + 1)*15,(donkeyY + 1)*15, 70, 50)
        pix = QPixmap('Images/Barrel.png')
        pixx = pix.scaled(QSize(70, 50))
        self.setPixmap(pixx)
        self.th = Thread(target=self.Fall, args=())
        self.th.start()

    def getPosition(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] >= 150:
                        self.BarrelX = x
                        self.BarrelY = y
                        return

    def printMap(self):
        for x in range(len(self.map)):
            row = []
            for y in range(len(self.map[x])):
                row.append(self.map[x][y])
            print(row)

    def Fall(self):
        while True:
            self.move(self.x() + 18, self.y())
            pix = QPixmap('Images/Barrel.png')
            pixx = pix.scaled(QSize(70, 50))
            self.setPixmap(pixx)
            self.map[self.BarrelX + 1][BarrelY] = self.map[self.BarrelX + 1][self.BarrelY] + 150
            self.map[self.BarrelX][BarrelY] = self.map[self.BarrelX][self.BarrelY] - 150
            self.map[self.BarrelX + 1][BarrelY + 1] = self.map[self.BarrelX + 1][self.BarrelY + 1] + 150
            self.map[self.BarrelX][BarrelY + 1] = self.map[self.BarrelX][self.BarrelY + 1] - 150
            #self.printMap()
            time.sleep(0.5)


class DonkeyKong(QLabel):
    def __init__(self, map, parent=None):
        super().__init__(parent)
        self.map = map
        self.DonkeyX = 0
        self.DonkeyY = 0
        self.setGeometry(262, 112, 70, 80)
        pix = QPixmap('Images/doKo.png')
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
                        pix = QPixmap('Images/doKo.png')
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
                        pix = QPixmap('Images/doKo.png')
                        pixx = pix.scaled(QSize(70, 80))
                        self.setPixmap(pixx)
                        for k in range(0, 4):
                            self.map[self.DonkeyX + k][self.DonkeyY + 4] = self.map[self.DonkeyX + k][self.DonkeyY + 4] + 6
                            self.map[self.DonkeyX + k][self.DonkeyY] = self.map[self.DonkeyX + k][self.DonkeyY] - 6
                        #self.printMap()
                        time.sleep(0.5)