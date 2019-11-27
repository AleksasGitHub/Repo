import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QSize


class Mover(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 50, 50)
        pix = QPixmap('ItsAMe.png')
        pixx = pix.scaled(QSize(50, 50))
        self.setPixmap(pixx)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.move(self.x(), self.y() - 15)
        elif event.key() == Qt.Key_Down:
            self.move(self.x(), self.y() + 15)
        elif event.key() == Qt.Key_Left:
            self.move(self.x() - 15, self.y())
        elif event.key() == Qt.Key_Right:
            self.move(self.x() + 15, self.y())
        else:
            QLabel.keyPressEvent(self, event)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.mover = Mover(centralWidget)
        self.mover.setFocus()
        self.setGeometry(400, 35, 600, 700)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())