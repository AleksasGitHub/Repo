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
from multiprocessing import Process, Pipe, Queue


class DonkeyKongServer():
    def __init__(self, queue: Queue, pipe: Pipe):
        super().__init__()
        self.queue = queue
        self.pipe = pipe
        self.kill = False
        self.barrels = []
        self.wait_throw = 2
        self.th = Thread(target=self.moveRandom, args=())
        self.th.start()
        self.player_thread = Thread(target=self.restart, args=())
        self.player_thread.start()

    def moveRandom(self):
        barrelCount = 0
        barrelRandom = random.randrange(3, 5)
        #self.first = True
        while not self.kill:
            i = random.randrange(0, 101, 1) % 2
            times = random.randrange(3, 5)
            if i == 0:
                for j in range(0, times):
                    self.queue.put("LEFT")
                    time.sleep(0.3)
            else:
                for j in range(0, times):
                    self.queue.put("RIGHT")
                    time.sleep(0.3)

            barrelCount += 1
            if barrelCount == barrelRandom:
                self.queue.put("Barrel")
                barrelCount = 0
                barrelRandom = random.randrange(3, 5)
                time.sleep(self.wait_throw)

    def restart(self):
        while not self.kill:
            try:
                self.pipe.recv()
                self.kill = True
                if self.wait_throw - 0.2 > 0.2:
                    self.wait_throw = self.wait_throw - 0.2
                time.sleep(2.5)
                self.kill = False
                self.th = Thread(target=self.moveRandom, args=())
                self.th.start()
            finally:
                pass
