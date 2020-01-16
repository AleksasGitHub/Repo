import math
import random

from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, \
    QGridLayout, QSizePolicy
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


class GameMap(Process):
    def __init__(self, queue: Queue, conns, pipe1: Pipe, pipe2: Pipe, end_queue: Queue, max_arg: int):
        super().__init__(target=self.__count__, args=[queue, conns, pipe1, pipe2, end_queue])

    def __count__(self, queue: Queue, conns, pipe1: Pipe, pipe2: Pipe, end_queue: Queue):
        self.queue = queue
        self.conns = conns
        self.pipe1 = pipe1
        self.pipe2 = pipe2
        self.end_queue = end_queue
        self.platforms1 = []
        self.platforms2 = []
        self.velocity = 1
        self.player1LoseLife = False
        self.player2LoseLife = False
        self.falling = True
        self.score1 = 0
        self.score2 = 0
        self.kill = False
        self.livesPlayer1 = 3
        self.livesPlayer2 = 3
        self.daemon = True
        self.map = \
            [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
             [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        while not self.kill:
            direction = self.queue.get()
            self.read_queue(direction)

    def read_queue(self, direction):
        if direction == "W" or direction == "A" or direction == "S" or direction == "D":
            x, y = self.readCoordinates("Player1")
            self.movePlayer(direction, x, y, 3, 4, 1)
        elif direction == "I" or direction == "J" or direction == "K" or direction == "L":
            x, y = self.readCoordinates("Player2")
            self.movePlayer(direction, x, y, 4, 3, 2)
        elif "PowerUp" in direction:
            chars = direction.split()
            self.setPowerUp(chars[1], chars[2])
        elif "Barrel" in direction:
            self.throw_barrel()
        elif direction == "LEFT" or direction == "RIGHT":
            x, y = self.readCoordinates("Donkey")
            self.moveDonkey(direction, x, y)

        self.checkPositionOfPlayers()

    def throw_barrel(self):
        self.falling = True
        x, y = self.readCoordinates("Donkey")
        text = 'T B ' + str(x + 2) + ' ' + str(y + 1) + ' '
        while len(text) < 10:
            text += 'A'
        for i in range(0, 2):
            self.conns[i].sendall(text.encode('utf8'))
        self.write(x + 2, y + 1, 31)
        self.write(x + 2, y + 2, 31)
        self.th = Thread(target=self.barrel_fall, args=(x + 2, y + 1,))
        self.th.start()

    def barrel_fall(self, x, y):
        k = 0
        while k < 27 and self.falling:
            if x < 34:
                self.write(x + 1, y, 31)
                self.write(x + 1, y + 1, 31)
            self.write(x, y, -31)
            self.write(x, y + 1, -31)
            x = x + 1
            k = k + 1
            time.sleep(self.velocity)

    def setPowerUp(self, x, y):
        self.write(int(x), int(y), 8)
        text = 'P ' + str(x) + ' ' + str(y) + ' '
        while len(text) < 10:
            text += 'A'
        for i in range(0, 2):
            self.conns[i].sendall(text.encode('utf8'))

    def checkPositionOfPlayers(self):
        x1, y1 = self.readCoordinates("Player1")
        x2, y2 = self.readCoordinates("Player2")
        legs1 = self.getCharacter(x1, y1)
        head1 = self.getCharacter(x1 - 1, y1)
        legs2 = self.getCharacter(x2, y2)
        head2 = self.getCharacter(x2 - 1, y2)

        self.player1LoseLife = False
        self.player2LoseLife = False
        self.checkLives(x1, y1, legs1, head1, 3, 4, 1)
        self.checkLives(x2, y2, legs2, head2, 4, 3, 2)
        if not self.player1LoseLife:
            self.checkScore(x1 + 1, 1)
        if not self.player2LoseLife:
            self.checkScore(x2 + 1, 2)
        self.checkLevel(x1, y1, legs1, 3, 4, 1)
        self.checkLevel(x2, y2, legs2, 4, 3, 2)
        self.checkPowerUp(x1, y1, legs1, head1, 3, 4, 1)
        self.checkPowerUp(x2, y2, legs2, head2, 4, 3, 2)

    def checkPowerUp(self, x, y, legs, head, playerValue, otherPlayerValue, playerID):
        b1 = legs == 8 + playerValue or legs == 10 + playerValue or legs == 8 + playerValue + otherPlayerValue or legs == 10 + playerValue + otherPlayerValue
        b2 = head == 8 + playerValue or head == 10 + playerValue or head == 8 + playerValue + otherPlayerValue or head == 10 + playerValue + otherPlayerValue
        if b1 or b2:
            i = random.randrange(0, 101, 1) % 2
            if i == 0:
                text = 'P L P ' + str(playerID) + ' AA'
                for i in range(0, 2):
                    self.conns[i].sendall(text.encode('utf8'))
                if playerID == 1 and self.livesPlayer1 != 0:
                    self.livesPlayer1 -= 1
                elif playerID == 2 and self.livesPlayer2 != 0:
                    self.livesPlayer2 -= 1
            else:
                text = 'P G P ' + str(playerID) + ' AA'
                for i in range(0, 2):
                    self.conns[i].sendall(text.encode('utf8'))
                if playerID == 1 and self.livesPlayer1 != 3:
                    self.livesPlayer1 += 1
                elif playerID == 2 and self.livesPlayer2 != 3:
                    self.livesPlayer2 += 1
            if b1:
                self.write(x, y, -8)
            else:
                self.write(x - 1, y, -8)
            text = 'P H AAAAAA'
            for i in range(0, 2):
                self.conns[i].sendall(text.encode('utf8'))

    def checkLives(self, x, y, legs, head, playerValue, otherPlayerValue, playerID):
        b = (playerValue + 16 <= legs <= 39 + playerValue) or (playerValue + 16 <= head <= 39 + playerValue)
        if b:
            text = 'L L P ' + str(playerID) + ' AA'
            for i in range(0, 2):
                self.conns[i].sendall(text.encode('utf8'))
            self.write(x, y, -playerValue)
            self.write(x - 1, y, -playerValue)
            if playerID == 1:
                self.write(34, 1, playerValue)
                self.write(33, 1, playerValue)
                self.player1LoseLife = True
                if self.livesPlayer1 - 1 >= 0:
                    self.livesPlayer1 -= 1
            else:
                self.write(34, 31, playerValue)
                self.write(33, 31, playerValue)
                self.player2LoseLife = True
                if self.livesPlayer2 - 1 >= 0:
                    self.livesPlayer2 -= 1

            if self.livesPlayer1 == 0 and self.livesPlayer2 == 0:
                for i in range(0, 3):
                    self.end_queue.put('End')
                self.kill = True

    def checkScore(self, x, playerID):
        if x == 5 or x == 10 or x == 15 or x == 20 or x == 25 or x == 30:
            if playerID == 1:
                if not self.platforms1.__contains__(x):
                    self.platforms1.append(x)
                    self.score1 += 1
                    text = 'S P ' + str(playerID) + ' ' + str(self.score1) + ' '
                    while len(text) < 10:
                        text += 'A'
                    for i in range(0, 2):
                        self.conns[i].sendall(text.encode('utf8'))
            else:
                if not self.platforms2.__contains__(x):
                    self.platforms2.append(x)
                    self.score2 += 1
                    text = 'S P ' + str(playerID) + ' ' + str(self.score2) + ' '
                    while len(text) < 10:
                        text += 'A'
                    for i in range(0, 2):
                        self.conns[i].sendall(text.encode('utf8'))

    def checkLevel(self, x, y, legs, player_value, other_player_value, playerID):
        b = legs == 80 + player_value or legs == 80 + player_value + other_player_value
        if b:
            if playerID == 1:
                self.score1 += 5
                text = 'S P ' + str(playerID) + ' ' + str(self.score1) + ' '
                while len(text) < 10:
                    text += 'A'
                for i in range(0, 2):
                    self.conns[i].sendall(text.encode('utf8'))
            else:
                self.score2 += 5
                text = 'S P ' + str(playerID) + ' ' + str(self.score2) + ' '
                while len(text) < 10:
                    text += 'A'
                for i in range(0, 2):
                    self.conns[i].sendall(text.encode('utf8'))

            self.pipe1.send('Restart')
            self.pipe2.send('Restart')

            if self.velocity - 0.1 > 0.1:
                self.velocity = self.velocity - 0.1
            self.falling = False

            text = 'Next Level'
            for i in range(0, 2):
                self.conns[i].sendall(text.encode('utf8'))

            self.platforms1 = []
            self.platforms2 = []
            if self.livesPlayer1 != 0:
                self.livesPlayer1 = 3
            if self.livesPlayer2 != 0:
                self.livesPlayer2 = 3
            self.restartMap()

    def moveDonkey(self, direction, x, y):
        if direction == "LEFT":
            character = self.getCharacter(x, y - 1)
            b = character != 1
            if b:
                # self.move(self.x() - 18, self.y())
                text = 'M D L AAAA'
                for i in range(0, 2):
                    self.conns[i].sendall(text.encode('utf8'))

                for k in range(0, 4):
                    self.write(x + k, y - 1, 16)
                    self.write(x + k, y + 3, -16)
        else:
            if y + 5 <= 32:
                character = self.getCharacter(x, y + 4)
                b = character != 1
                if b:
                    text = 'M D R AAAA'
                    for i in range(0, 2):
                        self.conns[i].sendall(text.encode('utf8'))

                    for k in range(0, 4):
                        self.write(x + k, y + 4, 16)
                        self.write(x + k, y, -16)

    def movePlayer(self, direction, x, y, playerValue, otherPlayerValue, playerID):
        if direction == "W" or direction == "I":
            character = self.getCharacter(x, y)
            b = character == 2 + playerValue or character == 2 + playerValue + otherPlayerValue or \
                character == 10 + playerValue + otherPlayerValue
            if b:
                if x > 31:
                    up = 19
                elif x > 26:
                    up = 20
                elif x > 21:
                    up = 19
                elif x > 16:
                    up = 20
                else:
                    up = 19

                # pomeranje slike
                text = 'M P ' + str(playerID) + ' U ' + str(up)
                for i in range(0, 2):
                    self.conns[i].sendall(text.encode('utf8'))

                # self.move(self.x(), self.y() - up)
                # self.previousX = self.PlayerX
                self.write(x, y, - playerValue)
                self.write(x - 2, y, playerValue)
                # self.getPosition()
                # self.newX = self.PlayerX
                # self.check_score(self.previousX, self.newX)

        elif direction == "S" or direction == "K":
            character = self.getCharacter(x + 1, y)
            self.printMap()
            b = character == 2 or character == 2 + otherPlayerValue or character == 10 + otherPlayerValue
            if b:
                if x > 31:
                    down = 19
                elif x > 26:
                    down = 20
                elif x > 21:
                    down = 19
                elif x > 16:
                    down = 20
                else:
                    down = 19

                text = 'M P ' + str(playerID) + ' D ' + str(down)
                for i in range(0, 2):
                    self.conns[i].sendall(text.encode('utf8'))

                # self.move(self.x(), self.y() + down)
                self.write(x + 1, y, playerValue)
                self.write(x - 1, y, -playerValue)

        elif direction == "A" or direction == "J":
            character = self.getCharacter(x, y - 1)
            b1 = character != 1
            if b1:
                character1 = self.getCharacter(x, y)
                character2 = self.getCharacter(x + 1, y)
                b2 = ((character2 == 2 and character1 == 2 + playerValue) or (
                        character2 == 2 + otherPlayerValue and character1 == 2 + playerValue) or (
                              character2 == 10 and character1 == 2 + playerValue) or (
                              character2 == 10 + otherPlayerValue and character1 == 2 + playerValue))
                if not b2:
                    text = 'M P ' + str(playerID) + ' L 18'
                    for i in range(0, 2):
                        self.conns[i].sendall(text.encode('utf8'))

                    self.write(x, y, -playerValue)
                    self.write(x - 1, y, -playerValue)
                    self.write(x, y - 1, playerValue)
                    self.write(x - 1, y - 1, playerValue)

        elif direction == "D" or direction == "L":
            character = self.getCharacter(x, y + 1)
            b1 = character != 1
            if b1:
                character1 = self.getCharacter(x, y)
                character2 = self.getCharacter(x + 1, y)
                b2 = ((character2 == 2 and character1 == 2 + playerValue) or (
                        character2 == 2 + otherPlayerValue and character1 == 2 + playerValue) or (
                              character2 == 10 and character1 == 2 + playerValue) or (
                              character2 == 10 + otherPlayerValue and character1 == 2 + playerValue))
                if not b2:
                    text = 'M P ' + str(playerID) + ' R 18'
                    for i in range(0, 2):
                        self.conns[i].sendall(text.encode('utf8'))

                    self.write(x, y, -playerValue)
                    self.write(x - 1, y, -playerValue)
                    self.write(x, y + 1, playerValue)
                    self.write(x - 1, y + 1, playerValue)

    def printMap(self):
        for x in range(len(self.map)):
            row = []
            for y in range(len(self.map[x])):
                row.append(self.map[x][y])
            print(row)

    def readCoordinates(self, character):
        self.X = -1
        self.Y = -1
        if character == "Player1":
            playerValue = 3
            otherPlayerValue = 4
            playerDrawn = 0
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    if self.map[x][y] == playerValue or self.map[x][y] == playerValue + 2 or self.map[x][y] \
                            == playerValue + otherPlayerValue or self.map[x][y] \
                            == playerValue + otherPlayerValue + 2 or self.map[x][y] \
                            == 16 + playerValue or self.map[x][y] \
                            == playerValue + otherPlayerValue + 16 or self.map[x][y] \
                            == 8 + playerValue or self.map[x][y] == 8 + playerValue + otherPlayerValue \
                            or self.map[x][y] == 31 + playerValue or self.map[x][y] == 31 \
                            + playerValue + otherPlayerValue or self.map[x][y] \
                            == 80 + playerValue or self.map[x][y] == 80 + playerValue + otherPlayerValue \
                            or self.map[x][y] == 18 + playerValue or self.map[x][y] == 18 \
                            + playerValue + otherPlayerValue or self.map[x][y] == 10 + playerValue or \
                            self.map[x][y] == 10 + playerValue + otherPlayerValue or self.map[x][y] == 33 + \
                            playerValue or self.map[x][y] == 33 + playerValue + otherPlayerValue or \
                            self.map[x][y] == 41 + playerValue or self.map[x][y] == 41 + playerValue + \
                            otherPlayerValue or self.map[x][y] == 49 + playerValue or self.map[x][y] == 49 \
                            + playerValue + otherPlayerValue or self.map[x][y] == 39 + \
                            playerValue or self.map[x][y] == 39 + playerValue + otherPlayerValue or \
                            self.map[x][y] == 47 + playerValue or self.map[x][y] == 47 + playerValue + \
                            otherPlayerValue:
                        if playerDrawn == 0:
                            playerDrawn = 1
                        else:
                            return x, y
        elif character == "Player2":
            playerValue = 4
            otherPlayerValue = 3
            playerDrawn = 0
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    if self.map[x][y] == playerValue or self.map[x][y] == playerValue + 2 or self.map[x][y] \
                            == playerValue + otherPlayerValue or self.map[x][y] \
                            == playerValue + otherPlayerValue + 2 or self.map[x][y] \
                            == 16 + playerValue or self.map[x][y] \
                            == playerValue + otherPlayerValue + 16 or self.map[x][y] \
                            == 8 + playerValue or self.map[x][y] == 8 + playerValue + otherPlayerValue \
                            or self.map[x][y] == 31 + playerValue or self.map[x][y] == 31 \
                            + playerValue + otherPlayerValue or self.map[x][y] \
                            == 80 + playerValue or self.map[x][y] == 80 + playerValue + otherPlayerValue \
                            or self.map[x][y] == 18 + playerValue or self.map[x][y] == 18 \
                            + playerValue + otherPlayerValue or self.map[x][y] == 10 + playerValue or \
                            self.map[x][y] == 10 + playerValue + otherPlayerValue or self.map[x][y] == 33 + \
                            playerValue or self.map[x][y] == 33 + playerValue + otherPlayerValue or \
                            self.map[x][y] == 41 + playerValue or self.map[x][y] == 41 + playerValue + \
                            otherPlayerValue or self.map[x][y] == 49 + playerValue or self.map[x][y] == 49 \
                            + playerValue + otherPlayerValue or self.map[x][y] == 39 + \
                            playerValue or self.map[x][y] == 39 + playerValue + otherPlayerValue or \
                            self.map[x][y] == 47 + playerValue or self.map[x][y] == 47 + playerValue + \
                            otherPlayerValue:
                        if playerDrawn == 0:
                            playerDrawn = 1
                        else:
                            return x, y
        elif character == "Donkey":
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    if self.map[x][y] == 16 or self.map[x][y] == 18 or self.map[x][y] == 21 or self.map[x][y] == 22 or \
                            self.map[x][y] == 25:
                        return x, y
        elif character == "Princess":
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    if self.map[x][y] == 28 or self.map[x][y] == 27 or self.map[x][y] == 31:
                        return x, y
        elif character == "PowerUp":
            self.X = self.Y = -1
            playerValue = 4
            otherPlayerValue = 3
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    if self.map[x][y] == 8 or self.map[x][y] == 10 or self.map[x][y] == 8 + playerValue or \
                            self.map[x][y] == 8 + otherPlayerValue or self.map[x][y] == 10 + playerValue or \
                            self.map[x][y] == 10 + otherPlayerValue or self.map[x][y] == \
                            10 + playerValue + otherPlayerValue or self.map[x][y] == 8 + playerValue \
                            + otherPlayerValue or self.map[x][y] == 41 or self.map[x][y] == 41 + playerValue \
                            or self.map[x][y] == 41 + otherPlayerValue or self.map[x][y] == 41 + playerValue \
                            + otherPlayerValue or self.map[x][y] == 39 or self.map[x][y] == 39 + playerValue \
                            or self.map[x][y] == 39 + otherPlayerValue or self.map[x][y] == 39 + playerValue \
                            + otherPlayerValue:
                        return x, y

    def getCharacter(self, x: int, y: int):
        return self.map[x][y]

    def write(self, x: int, y: int, value: int):
        self.map[x][y] = self.map[x][y] + value

    def restartMap(self):
        self.map = \
            [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
             [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def check_end(self):
        self.end_queue.get()
        self.kill = True
