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

class Princess(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(260, 20, 50, 70)
        pix = QPixmap('peach2.png')
        pixx = pix.scaled(QSize(50, 70))
        self.setPixmap(pixx)
        self.th = Thread(target=self.wave, args=())
        self.th.start()

    def wave(self):
        while True:
            pix = QPixmap('wave.png')
            pixx = pix.scaled(QSize(50, 70))
            self.setPixmap(pixx)
            time.sleep(0.5)
            pix2 = QPixmap('peach2.png')
            pixx2 = pix2.scaled(QSize(50, 70))
            self.setPixmap(pixx2)
            time.sleep(0.5)

