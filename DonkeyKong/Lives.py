
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, QtGui
import sys
import time
from tkinter import *
import threading
from threading import Thread

class Lives(QLabel):
    def __init__(self, lives,  parent=None):
        super().__init__(parent)
        self.lives = lives
        self.lose_life(self.lives)

    def lose_life(self, lives):
        self.lives = lives
        if self.lives == 3:
            self.setGeometry(9, 10, 100, 70)
            pix = QPixmap('3hearts.jpg')
            pixx = pix.scaled(QSize(100, 70))
            self.setPixmap(pixx)
        elif self.lives == 2:
            self.setGeometry(9, 10, 100, 70)
            pix = QPixmap('2hearts.jpg')
            pixx = pix.scaled(QSize(100, 70))
            self.setPixmap(pixx)
        elif self.lives == 1:
            self.setGeometry(9, 10, 100, 70)
            pix = QPixmap('1heart.jpg')
            pixx = pix.scaled(QSize(100, 70))
            self.setPixmap(pixx)

