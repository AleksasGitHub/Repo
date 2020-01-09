import random
import time
from multiprocessing import Queue, Pipe
from threading import Thread

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class PowerUpServer():
    def __init__(self, queue: Queue, pipe: Pipe):
        self.queue = queue
        self.pipe = pipe
        self.kill = False
        self.player_thread = Thread(target=self.restart, args=[])
        self.player_thread.start()
        self.start_thread = Thread(target=self.start, args=[])
        self.start_thread.start()

    def start(self):
        x = random.randrange(0, 4)
        y = random.randrange(0, 31)
        times = random.randrange(25, 50)
        for i in range(0, times):
            time.sleep(0.1)
        self.queue.put("PowerUp %d %d" % (x * 5 + 14, y + 1))

    def restart(self):
        while not self.kill:
            try:
                self.pipe.recv()
                time.sleep(1.3)
                self.start_thread = Thread(target=self.start, args=[])
                self.start_thread.start()
            finally:
                pass