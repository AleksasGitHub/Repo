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


class PowerUp(QLabel):
    def __init__(self, x, y, parent=None):
        super().__init__(parent)
        self.row = 263 + x * 97
        self.column = 9 + y * 18
        self.setGeometry(self.column, self.row, 20, 20)  # 263 + x*97 - redovi; 9 + y*18 - kolone
        self.kill = False
        pix = QPixmap('Images/PowerUp.png')
        pixx = pix.scaled(QSize(20, 20))
        self.setPixmap(pixx)
        self.th = Thread(target=self.jump, args=())
        self.th.start()

    def jump(self):
        while not self.kill:
            self.setGeometry(self.column, self.row - 5, 20, 20)
            time.sleep(0.5)
            self.setGeometry(self.column, self.row, 20, 20)
            time.sleep(0.5)

