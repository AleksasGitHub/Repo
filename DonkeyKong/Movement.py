import math
import random

from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, QtGui
from Lives import Lives
import sys
import time
from tkinter import *
import threading
from threading import Thread
from multiprocessing import Process, Pipe, Queue
from RWLock import RWLock


class MovementProcess(Process):
    def __init__(self, player1: Pipe, player2: Pipe, main_process: Queue, max_arg: int):
        super().__init__(target=self.__count__, args=(player1, player2, main_process, ))

    def __count__(self, player1: Pipe, player2: Pipe, main_process: Queue):
        self.player1_pipe = player1
        self.player2_pipe = player2
        self.main_process_queue = main_process
        self.kill = False

        while not self.kill:
            self.movement = self.main_process_queue.get()
            if self.movement == "W" or self.movement == "A" or self.movement == "S" or self.movement == "D":
                self.player1_pipe.send(self.movement)
            else:
                self.player2_pipe.send(self.movement)