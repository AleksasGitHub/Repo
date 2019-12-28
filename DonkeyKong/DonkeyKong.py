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
    def __init__(self, map, donkeyX, donkeyY, my_obj_rwlock, parent = None):
        super().__init__(parent)
        self.map = map
        self.BarrelX = donkeyX + 2
        self.BarrelY = donkeyY + 1
        self.my_obj_rwlock = my_obj_rwlock

        with self.my_obj_rwlock.w_locked():
            self.map[self.BarrelX][self.BarrelY] = self.map[self.BarrelX][self.BarrelY] + 31
            self.map[self.BarrelX][self.BarrelY + 1] = self.map[self.BarrelX][self.BarrelY + 1] + 31
        self.setGeometry(200, 200, 70, 50) # naci prave kordinate
        pix = QPixmap('Images/Barrel.png')
        pixx = pix.scaled(QSize(70, 50))
        self.setPixmap(pixx)
        self.printMap()
        self.th = Thread(target=self.Fall, args=())
        self.th.start()

    def getPosition(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                with self.my_obj_rwlock.r_locked():
                    if 31 <= self.map[x][y] <= 38 or self.map[x][y] == 47 or self.map[x][y] == 49 or 40 <= self.map[x][y] <= 43:
                            self.BarrelX = x
                            self.BarrelY = y
                            return

    def printMap(self):
        for x in range(len(self.map)):
            row = []
            with self.my_obj_rwlock.r_locked():
                for y in range(len(self.map[x])):
                    row.append(self.map[x][y])
            print(row)

    def Fall(self):
        self.getPosition()
        for k in range(0, 27):
            self.getPosition()
            self.move(self.x() + 18, self.y())
            pix = QPixmap('Images/Barrel.png')
            pixx = pix.scaled(QSize(70, 50))
            self.setPixmap(pixx)
            with self.my_obj_rwlock.w_locked():
                if(self.BarrelX < 34):
                    self.map[self.BarrelX + 1][self.BarrelY] = self.map[self.BarrelX + 1][self.BarrelY] + 31
                    self.map[self.BarrelX + 1][self.BarrelY + 1] = self.map[self.BarrelX + 1][self.BarrelY + 1] + 31
                self.map[self.BarrelX][self.BarrelY] = self.map[self.BarrelX][self.BarrelY] - 31
                self.map[self.BarrelX][self.BarrelY + 1] = self.map[self.BarrelX][self.BarrelY + 1] - 31
            #self.printMap()
            time.sleep(0.5)
            self.getPosition()


class DonkeyKong(QLabel):
    def __init__(self, map, hbox, my_obj_rwlock, parent=None):
        super().__init__(parent)
        self.map = map
        self.hbox = hbox
        self.DonkeyX = 0
        self.DonkeyY = 0
        self.kill = False
        self.setGeometry(262, 112, 70, 80)
        pix = QPixmap('Images/doKo.png')
        pixx = pix.scaled(QSize(70, 80))
        self.setPixmap(pixx)
        self.my_obj_rwlock = my_obj_rwlock
        self.th = Thread(target=self.moveRandom, args=())
        self.th.start()

    def getPosition(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                with self.my_obj_rwlock.r_locked():
                    if self.map[x][y] == 16 or self.map[x][y] == 18:
                            self.DonkeyX = x
                            self.DonkeyY = y
                            return

    def printMap(self):
        for x in range(len(self.map)):
            row = []
            for y in range(len(self.map[x])):
                with self.my_obj_rwlock.r_locked():
                    row.append(self.map[x][y])
            print(row)
        print()

    def moveRandom(self):
        first = True
        barrelCount = 0
        barrelRandom = random.randrange(3, 5)
        while not self.kill:
            i = random.randrange(0, 101, 1) % 2
            times = random.randrange(3, 5)
            self.getPosition()
            if i == 0:
                for j in range(0, times):
                    self.getPosition()
                    with self.my_obj_rwlock.r_locked():
                        b = self.map[self.DonkeyX][self.DonkeyY - 1] != 1
                    if b:
                    #if self.x() - 18 >= 0: #Provera pomeranja po mapi
                        self.move(self.x() - 18, self.y())
                        pix = QPixmap('Images/doKo.png')
                        pixx = pix.scaled(QSize(70, 80))
                        self.setPixmap(pixx)
                        with self.my_obj_rwlock.w_locked():
                            for k in range(0, 4):
                                self.map[self.DonkeyX + k][self.DonkeyY - 1] = self.map[self.DonkeyX + k][self.DonkeyY - 1] + 16
                                self.map[self.DonkeyX + k][self.DonkeyY + 3] = self.map[self.DonkeyX + k][self.DonkeyY + 3] - 16
                        #self.printMap()
                        time.sleep(0.5)
                barrelCount = barrelCount + 1

            else:
                for j in range(0, times):
                    self.getPosition()
                    if self.DonkeyY + 5 <= 32:
                        with self.my_obj_rwlock.r_locked():
                            b = self.map[self.DonkeyX][self.DonkeyY + 4] != 1
                        if b:
                        #if self.x() + 18 <= 510:
                            self.move(self.x() + 18, self.y())
                            pix = QPixmap('Images/doKo.png')
                            pixx = pix.scaled(QSize(70, 80))
                            self.setPixmap(pixx)
                            with self.my_obj_rwlock.r_locked():
                                for k in range(0, 4):
                                    self.map[self.DonkeyX + k][self.DonkeyY + 4] = self.map[self.DonkeyX + k][self.DonkeyY + 4] + 16
                                    self.map[self.DonkeyX + k][self.DonkeyY] = self.map[self.DonkeyX + k][self.DonkeyY] - 16
                            #self.printMap()
                            time.sleep(0.5)
                barrelCount = barrelCount + 1

            if barrelCount == barrelRandom: # and first:
                barrelCount = 0
                first = False
                barrelRandom = random.randrange(3, 5)
                self.getPosition()
                #self.BarrelWidget = QWidget()
                #self.hbox.addWidget(self.BarrelWidget, 1, 1)
                #self.barrel = Barrel(self.map, self.DonkeyX, self.DonkeyY, self.my_obj_rwlock, self.BarrelWidget)
                time.sleep(2)
