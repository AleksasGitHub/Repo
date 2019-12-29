import random
import time
from multiprocessing import Pipe
from threading import Thread

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class PowerUp(QLabel):
    def __init__(self, pipe: Pipe, my_obj_rwlock, parent=None):
        super().__init__(parent)
        self.x = random.randrange(0, 4)
        self.y = random.randrange(0, 31)
        self.my_obj_rwlock = my_obj_rwlock
        self.pipe = pipe
        with self.my_obj_rwlock.w_locked():
                self.pipe.send("write %d %d 8" % (self.x * 5 + 14, self.y + 1))
        #self.map[self.x * 5 + 14][self.y + 1] = self.map[self.x * 5 + 14][self.y + 1] + 8
        self.row = 263 + self.x * 97
        self.column = 9 + self.y * 18
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

