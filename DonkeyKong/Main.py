from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt
import sys
import  time
import  threading
from threading import  Thread


class PrincessWave(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(260, 20, 70, 70)
        pix = QPixmap('wave.png')
        pixx = pix.scaled(QSize(70, 70))
        self.setPixmap(pixx)

    def wave_function(self,):
        while 1:

         time.sleep(1)


class Princess(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(260, 20, 70, 70)
        pix = QPixmap('peach2.png')
        pixx = pix.scaled(QSize(70, 70))
        self.setPixmap(pixx)


class Mover(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 608, 70, 70)
        pix = QPixmap('ItsAMeRight.png')
        pixx = pix.scaled(QSize(70, 70))
        self.setPixmap(pixx)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.move(self.x(), self.y() - 15)
        elif event.key() == Qt.Key_Down:
            if self.y() + 15 <= 610:
                self.move(self.x(), self.y() + 15)
        elif event.key() == Qt.Key_Left:
            if self.x() - 5 >= -25:
                self.move(self.x() - 5, self.y())
                pix = QPixmap('ItsAMeLeft.png')
                pixx = pix.scaled(QSize(70, 70))
                self.setPixmap(pixx)
        elif event.key() == Qt.Key_Right:
            if self.x() + 5 <= 532:
                self.move(self.x() + 5, self.y())
                pix = QPixmap('ItsAMeRight.png')
                pixx = pix.scaled(QSize(70, 70))
                self.setPixmap(pixx)
        else:
            QLabel.keyPressEvent(self, event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.startButton = QPushButton("New Game", self)
        self.startButton.resize(100, 32)
        self.startButton.move(100, 500)
        self.startButton.clicked.connect(self.on_start)

        oImage = QImage("dk1.png")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.hbox = QGridLayout()
        self.hbox.setColumnStretch(1, 4)
        self.hbox.setRowStretch(1, 4)

        self.hbox.addWidget(self.startButton)
        self.setLayout(self.hbox)



        self.setGeometry(400, 35, 600, 700)
        self.show()



    def on_start(self):
        oImage = QImage("Background.png")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.startButton.hide()

        self.PrincessWidget = QWidget()
        self.MarioWidget = QWidget()

        #self.PrincessWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.hbox.addWidget(self.PrincessWidget,1,1)
        #self.MarioWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.hbox.addWidget(self.MarioWidget,1,1)

        self.mover = Mover(self.MarioWidget)
        self.princess = Princess(self.PrincessWidget)
        self.mover.setFocus()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    main = MainWindow()
    #x = threading.Thread(target=PrincessWave.wave_function,args=(1,))
    #x.start()
    sys.exit(app.exec_())
