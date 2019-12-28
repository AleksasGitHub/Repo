from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy

from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt

class Score(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: black; color: white; font-size:18px; font: bold System")
        self.setText("0")

    def change_score(self, score):
       self.score = score
       self.setText(format(str(self.score)))

    def text(self, player):
        if player==1:
          pix = QPixmap('Images/pl1.png')
          pixx = pix.scaled(QSize(100, 18))
          self.setPixmap(pixx)
        else:
            pix = QPixmap('Images/pl2.png')
            pixx = pix.scaled(QSize(100, 18))
            self.setPixmap(pixx)