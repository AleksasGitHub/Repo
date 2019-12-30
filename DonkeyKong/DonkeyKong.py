import math
import multiprocessing
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
from multiprocessing import Process, Pipe


class DonkeyKong(QLabel):
    def __init__(self, pipe: Pipe, player_pipe: Pipe, my_obj_rwlock, parent=None):
        super().__init__(parent)
        self.pipe = pipe
        self.player_pipe = player_pipe
        self.DonkeyX = 0
        self.DonkeyY = 0
        self.setGeometry(262, 112, 70, 80)
        pix = QPixmap('Images/doKo.png')
        pixx = pix.scaled(QSize(70, 80))
        self.setPixmap(pixx)
        self.my_obj_rwlock = my_obj_rwlock
        self.barrels = []
        self.wait_throw = 2
        self.th = Thread(target=self.moveRandom, args=())
        self.th.start()
        self.player_thread = Thread(target=self.restart, args=())
        self.player_thread.start()

    def getPosition(self):
        with self.my_obj_rwlock.w_locked():
            self.pipe.send("readCoordinates Donkey")
            s = self.pipe.recv()
            char = s.split()
            self.DonkeyX = int(char[0])
            self.DonkeyY = int(char[1])

    def moveRandom(self):
        barrelCount = 0
        barrelRandom = random.randrange(3, 5)
        while True:
            i = random.randrange(0, 101, 1) % 2
            times = random.randrange(3, 5)
            self.getPosition()
            if i == 0:
                for j in range(0, times):
                    self.getPosition()
                    with self.my_obj_rwlock.w_locked():
                        self.pipe.send("getCharacter %d %d" % (self.DonkeyX, self.DonkeyY - 1))
                        character = self.pipe.recv()
                        b = character != 1
                    if b:
                        self.move(self.x() - 18, self.y())
                        pix = QPixmap('Images/doKo.png')
                        pixx = pix.scaled(QSize(70, 80))
                        self.setPixmap(pixx)
                        with self.my_obj_rwlock.w_locked():
                            for k in range(0, 4):
                                self.pipe.send("write %d %d 16" % (self.DonkeyX + k, self.DonkeyY - 1))
                                self.pipe.send("write %d %d -16" % (self.DonkeyX + k, self.DonkeyY + 3))
                        time.sleep(0.3)
                barrelCount = barrelCount + 1

            else:
                for j in range(0, times):
                    self.getPosition()
                    if self.DonkeyY + 5 <= 32:
                        with self.my_obj_rwlock.w_locked():
                            self.pipe.send("getCharacter %d %d" % (self.DonkeyX, self.DonkeyY + 4))
                            character = self.pipe.recv()
                            b = character != 1
                        if b:
                            self.move(self.x() + 18, self.y())
                            pix = QPixmap('Images/doKo.png')
                            pixx = pix.scaled(QSize(70, 80))
                            self.setPixmap(pixx)
                            with self.my_obj_rwlock.w_locked():
                                for k in range(0, 4):
                                    self.pipe.send("write %d %d 16" % (self.DonkeyX + k, self.DonkeyY + 4))
                                    self.pipe.send("write %d %d -16" % (self.DonkeyX + k, self.DonkeyY))
                            time.sleep(0.3)
                barrelCount = barrelCount + 1

            if barrelCount == barrelRandom: # and first:
                barrelCount = 0
                barrelRandom = random.randrange(3, 5)
                self.getPosition()
                for i in range(0, 15):
                    if not self.barrels[i].falling:
                        self.barrels[i].StartFalling()
                        break
                time.sleep(self.wait_throw)

    def restart(self):
        while True:
            self.player_pipe.recv()
            self.setGeometry(262, 112, 70, 80)
            if self.wait_throw - 0.2 > 0.2:
                self.wait_throw = self.wait_throw - 0.2
            for i in range(0, len(self.barrels)):
                if self.barrels[i].falling:
                    self.barrels[i].falling = False
                if self.barrels[i].velocity - 0.1 > 0.1:
                    self.barrels[i].velocity = self.barrels[i].velocity - 0.1
                self.barrels[i].hide()
            with self.my_obj_rwlock.w_locked():
                self.pipe.send('deleteBarrels')
            time.sleep(1.3)


class Barrel(QLabel):
    def __init__(self, pipe: Pipe, my_obj_rwlock, donkey: DonkeyKong, parent=None):
        super().__init__(parent)
        self.hide()
        self.pipe = pipe
        self.my_obj_rwlock = my_obj_rwlock
        self.donkey = donkey
        self.falling = False
        self.velocity = 1
        self.donkey.barrels.append(self)
        self.index = len(self.donkey.barrels) - 1

    def StartFalling(self):
        self.falling = True
        self.show()
        with self.my_obj_rwlock.w_locked():
            self.pipe.send("readCoordinates Donkey")
            s = self.pipe.recv()
            char = s.split()
            self.DonkeyX = int(char[0])
            self.DonkeyY = int(char[1])
        BarrelX = self.DonkeyX + 2
        BarrelY = self.DonkeyY + 1
        with self.my_obj_rwlock.w_locked():
            self.pipe.send("write %d %d 31" % (BarrelX, BarrelY))
            self.pipe.send("write %d %d 31" % (BarrelX, BarrelY + 1))
        self.setGeometry(self.DonkeyY * 18, 140, 50, 30) # naci prave kordinate
        with self.my_obj_rwlock.w_locked():
            self.pipe.send("printMap")
        pix = QPixmap('Images/Barrel.png')
        pixx = pix.scaled(QSize(50, 30))
        self.setPixmap(pixx)
        self.th = Thread(target=self.Fall, args=(BarrelX, BarrelY, ))
        self.th.start()

    def Fall(self, BarrelX, BarrelY):
        k = 0
        while self.falling and k < 27:
            self.move(self.x(), self.y() + 18)
            with self.my_obj_rwlock.w_locked():
                if BarrelX < 34:
                    self.pipe.send("write %d %d 31" % (BarrelX + 1, BarrelY))
                    self.pipe.send("write %d %d 31" % (BarrelX + 1, BarrelY + 1))
                self.pipe.send("write %d %d -31" % (BarrelX, BarrelY))
                self.pipe.send("write %d %d -31" % (BarrelX, BarrelY + 1))
                #self.pipe.send("printMap")
            BarrelX = BarrelX + 1
            k = k + 1
            time.sleep(self.velocity)
        with self.my_obj_rwlock.w_locked():
            self.pipe.send("printMap")
        self.falling = False
        self.hide()

    def deleteCoordinates(self):
        currentBarrelX = self.donkey.barrels[self.index].BarrelX
        currentBarrelY = self.donkey.barrels[self.index].BarrelY
        with self.my_obj_rwlock.w_locked():
            self.pipe.send("write %d %d -31" % (currentBarrelX, currentBarrelY))
            self.pipe.send("write %d %d -31" % (currentBarrelX, currentBarrelY + 1))
            # self.pipe.send("printMap")