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
        self.map[self.BarrelX][self.BarrelY] = self.map[self.BarrelX][self.BarrelY] + 150
        self.map[self.BarrelX][self.BarrelY + 1] = self.map[self.BarrelX][self.BarrelY + 1] + 150
        self.setGeometry(200, 100, 70, 50) # naci prave kordinate
        pix = QPixmap('Images/doKo.png')
        pixx = pix.scaled(QSize(70, 50))
        self.setPixmap(pixx)
        self.printMap()
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
        self.getPosition()
        for k in range(0, 27):
            self.move(self.x() + 18, self.y())
            pix = QPixmap('Images/doKo.png')
            pixx = pix.scaled(QSize(70, 50))
            self.setPixmap(pixx)
            if(self.BarrelX < 34):
                self.map[self.BarrelX + 1][self.BarrelY] = self.map[self.BarrelX + 1][self.BarrelY] + 150
                self.map[self.BarrelX + 1][self.BarrelY + 1] = self.map[self.BarrelX + 1][self.BarrelY + 1] + 150
            self.map[self.BarrelX][self.BarrelY] = self.map[self.BarrelX][self.BarrelY] - 150
            self.map[self.BarrelX][self.BarrelY + 1] = self.map[self.BarrelX][self.BarrelY + 1] - 150
            self.printMap()
            time.sleep(0.5)
            self.getPosition()


class DonkeyKong(QLabel):
    def __init__(self, map, hbox, parent=None):
        super().__init__(parent)
        self.map = map
        self.hbox = hbox
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
                if self.map[x][y] == 6 or self.map[x][y] == 8: #or #(self.map[x][y] >= 9 and self.map[x][y] <= 150):
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
        first = True
        barrelCount = 0
        barrelRandom = random.randrange(3, 5)
        while True:
            i = random.randrange(0, 101, 1) % 2
            times = random.randrange(3, 5)
            self.getPosition()
            if i == 0:
                for j in range(0, times):
                    if self.map[self.DonkeyX][self.DonkeyY - 1] != 1:
                    #if self.x() - 18 >= 0: #Provera pomeranja po mapi
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
                barrelCount = barrelCount + 1

            else:
                for j in range(0, times):
                    if self.DonkeyY + 5 <= 32:
                        if self.map[self.DonkeyX][self.DonkeyY + 5] != 1:
                        #if self.x() + 18 <= 510:
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
                barrelCount = barrelCount + 1

            if barrelCount == barrelRandom and first:
                barrelCount = 0
                first = False
                barrelRandom = random.randrange(3, 5)
                self.getPosition()
                self.Barrel = QWidget()
                self.hbox.addWidget(self.Barrel, 1, 1)
                self.barrel = Barrel(self.map, self.DonkeyX, self.DonkeyY)
                time.sleep(2)
