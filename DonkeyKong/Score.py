from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy



class Score(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: black; color: white; font-size:18px; font: bold")
        self.setText("0")
        self.setGeometry(440, 10, 100, 70)

    def change_score(self, score):
       self.score = score
       self.setText(format(str(self.score)))