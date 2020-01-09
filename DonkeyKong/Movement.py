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
    def __init__(self, player1: Pipe, player2: Pipe, main_process: Queue, socket, max_arg: int):
        super().__init__(target=self.__count__, args=(player1, player2, main_process, socket, ))

    def __count__(self, player1: Pipe, player2: Pipe, main_process: Queue, socket):
        self.player1_pipe = player1
        self.player2_pipe = player2
        self.main_process_queue = main_process
        self.kill = False
        self.socket = socket

        while not self.kill:
            self.movement = self.main_process_queue.get()
            if self.movement == "W" or self.movement == "A" or self.movement == "S" or self.movement == "D":
                if socket is None:
                    self.player1_pipe.send(self.movement)
                else:
                    socket.send(self.movement.encode('utf8'))
            elif self.movement == "I" or self.movement == "J" or self.movement == "K" or self.movement == "L":
                if socket is None:
                    self.player2_pipe.send(self.movement)
                else:
                    socket.send(self.movement.encode('utf8'))