
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, QtGui
import sys
import time


class Level(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent; color: white; font-size:18px; font: bold System")
        self.setText("1")
        self.setGeometry(274, -8, 100, 70)
        self.level = 1

    def level_up(self):
         self.level = self.level + 1
         self.setText(format(str(self.level)))

    def game_over(self):
        self.level = 1
        self.setText(format(str(self.level)))