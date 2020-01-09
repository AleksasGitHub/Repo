import math
import random
import socket

from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, QtGui
from Mover import Mover
from DonkeyKong import DonkeyKong, Barrel
from Princess import Princess
from Lives import Lives
from  Score import  Score
from Level import Level
import sys
import time
from tkinter import *
import threading
from threading import Thread
from RWLock import RWLock
import multiprocessing as mp
import Map
import Movement
from PowerUp import PowerUp

HOST = 'localhost'
PORT = 50005


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('Images/doKo.png'))
        self.setWindowTitle("Donkey Kong")
        self.firstTime = True
        self.hbox = QGridLayout()
        self.hbox.setHorizontalSpacing(0)
        self.hbox.setVerticalSpacing(0)
        self.hbox.setColumnStretch(1, 4)
        self.hbox.setRowStretch(1, 4)
        self.initUI()

    def initUI(self):
        self.game_started = False
        self.online_game = False

        self.startButton = QPushButton("New Game", self)
        self.startButton.resize(100, 32)
        self.startButton.setGeometry(130, 600, 100, 32)
        self.startButton.setStyleSheet("background-color: green; color: white; font-size:14px; font: bold System")
        self.startButton.clicked.connect(self.on_start)
        self.startButton.show()

        self.onlineButton = QPushButton("Online Game", self)
        self.onlineButton.resize(100, 32)
        self.onlineButton.setGeometry(248, 600, 100, 32)
        self.onlineButton.setStyleSheet("background-color: yellow; color: white; font-size:14px; font: bold System")
        self.onlineButton.clicked.connect(self.on_online)
        self.onlineButton.show()

        self.exitButton = QPushButton("Exit", self)
        self.exitButton.resize(100, 32)
        self.exitButton.setGeometry(360, 600, 100, 32)
        self.exitButton.setStyleSheet("background-color: red; color: white; font-size:14px; font: bold System")
        self.exitButton.clicked.connect(self.exit_game)
        self.exitButton.show()

        self.menuButton = QPushButton("Menu", self)
        self.menuButton.resize(100, 32)
        self.menuButton.setGeometry(230, 500, 100, 32)
        self.menuButton.setStyleSheet("background-color: green; color: white; font-size:14px; font: bold System")
        self.menuButton.clicked.connect(self.showHideWdigets)
        self.menuButton.hide()

        self.ScoreLabelText = QLabel("Score: 0", self)
        self.scoreLabelText = Score(self.ScoreLabelText)
        self.scoreLabelText.setGeometry(70, 278, 100, 18)
        self.scoreLabelText.text(1)
        self.ScoreLabelText.hide()

        self.ScoreLabelText2 = QLabel("Score: 0", self)
        self.scoreLabelText2 = Score(self.ScoreLabelText2)
        self.scoreLabelText2.setGeometry(370, 278, 100, 18)
        self.scoreLabelText2.text(2)
        self.ScoreLabelText2.hide()

        self.ScoreLabelMover1 = QLabel("Score: 0", self)
        self.scoreLabelMover1 = Score(self.ScoreLabelMover1)
        self.scoreLabelMover1.setGeometry(120, 348, 100, 38)
        self.ScoreLabelMover1.hide()

        self.ScoreLabelMover2 = QLabel("Score: 0", self)
        self.scoreLabelMover2 = Score(self.ScoreLabelMover2)
        self.scoreLabelMover2.setGeometry(420, 348, 100, 38)
        self.ScoreLabelMover2.hide()

        self.ScoreLabelResult = QLabel("Score: 0", self)
        self.scoreLabelResult = Score(self.ScoreLabelResult)
        self.scoreLabelResult.setGeometry(210, 148, 300, 38)
        self.scoreLabelResult.setStyleSheet("background-color: black; color: red; font-size:18px; font: bold System")
        self.ScoreLabelResult.hide()

        self._height = 600
        self._width = 500
        self.image_size = 18

        oImage = QImage("Images/dk1.png")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        '''self.hbox = QGridLayout()
        self.hbox.setHorizontalSpacing(0)
        self.hbox.setVerticalSpacing(0)
        self.hbox.setColumnStretch(1, 4)
        self.hbox.setRowStretch(1, 4)'''

        self.setLayout(self.hbox)

        self.setGeometry(400, 35, 600, 700)

        self.hbox.update()
        self.show()

    def on_online(self):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            #slika wait
            text = ''
            bin = s.recv(1024)
            text += str(bin, 'utf-8')
            if text.split()[0] == "Player":
                print('Received', text)
                if text.split()[1] == '1':
                    pass
                else:
                    pass
                #slika da ce igra poceti
                self.start_online_game(s)
            else:
                print('Error, please try again later')
                #vrati na meni

    def start_online_game(self, s):
        self.game_started = True
        self.online_game = True

        oImage = QImage("Images/Background2.png")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.startButton.hide()
        self.exitButton.hide()
        self.onlineButton.hide()

        self.initialize()

        self.initialize_level_and_lives()
        self.powerUp = PowerUp(None, None, None, self.PowerUpWidget)
        self.donkey = DonkeyKong(None, None, None, None, self.DonkeyWidget)
        self.donkey_barrels = []
        for i in range(0, 15):
            self.donkey_barrels.append(Barrel(None, None, self.donkey, self.barrels[i]))
        self.mover1 = Mover(self.next_level, None, None, None, None, None, self.livesWidget1, self.levelLabel,
                            self.scoreLabel1, None, True, None, self.PowerUpWidget, self.MarioWidget1)
        self.mover2 = Mover(self.next_level, None, None, None, None, None, self.livesWidget2, self.levelLabel,
                            self.scoreLabel2, None, False, None, self.PowerUpWidget, self.MarioWidget2)
        self.princess = Princess(self.PrincessWidget)

        self.queue = mp.Queue()
        self.movement_process = Movement.MovementProcess(None, None, self.queue, s, max_arg=101)
        self.movement_process.start()

        self.th = Thread(target=self.check_for_game_end, args=())
        self.th.do_run = True
        self.th.start()

        self.hbox.update()

        self.thread_commands = Thread(target=self.receive_commands, args=(s,))
        self.thread_commands.start()

    def receive_commands(self, s):
        while True:
            text = ''
            bin = s.recv(10)
            text += str(bin, 'utf-8')
            if not bin or len(bin) < 1024:
                pass
            char = text.split()
            if char[0] == 'M':
                if char[1] == 'P':
                    if char[2] == '1':
                        self.mover1.move_online_player(char[3], char[4])
                    else:
                        self.mover2.move_online_player(char[3], char[4])
                elif char[1] == "D":
                    self.donkey.move_online(char[2])
            elif char[0] == 'L':
                if char[3] == '1':
                    self.mover1.loseLife(self.livesWidget1)
                else:
                    self.mover2.loseLife(self.livesWidget2)
            elif char[0] == "P":
                if char[1] == "G":
                    if char[3] == "1":
                        self.mover1.gainLifePowerUp(self.livesWidget1)
                    else:
                        self.mover2.gainLifePowerUp(self.livesWidget2)
                elif char[1] == "L":
                    if char[3] == "1":
                        self.mover1.loseLifePowerUp(self.livesWidget1)
                    else:
                        self.mover2.loseLifePowerUp(self.livesWidget2)
                elif char[1] == "H":
                    self.powerUp.hideYourself()
                else:
                    self.powerUp.setPosition(char[1], char[2])
            elif char[0] == 'S':
                if char[2] == '1':
                    self.mover1.updateScore(char[3])
                else:
                    self.mover2.updateScore(char[3])
            elif char[0] == 'Next':
                self.mover1.nextLevel(self.levelLabel, self.livesWidget1)
                self.mover2.nextLevel(self.levelLabel, self.livesWidget2)
                self.donkey.nextLevel()
            elif char[0] == 'T':
                self.donkey.throw_barrel(char[2], char[3])
            if "D" not in text:
                print('Received', text)

    def exit_game(self):
        self.close()

    def initialize(self):
        self.my_obj_rwlock = RWLock()

        self.PrincessWidget = QWidget()
        self.MarioWidget1 = QWidget()
        self.MarioWidget2 = QWidget()
        self.DonkeyWidget = QWidget()
        self.LivesWidget1 = QWidget()
        self.ScoreLabel1 = QLabel("", self)
        self.LivesWidget2 = QWidget()
        self.ScoreLabel2 = QLabel("", self)
        self.LevelLabel = QLabel("", self)
        self.NextLevelLabel = QLabel("", self)
        self.PowerUpWidget = QWidget()
        self.barrels = []
        for i in range(0, 15):
            self.barrels.append(QWidget())

        self.hbox.addWidget(self.ScoreLabel1, 1, 1)
        self.hbox.addWidget(self.ScoreLabel2, 1, 1)
        self.hbox.addWidget(self.LevelLabel, 1, 1)
        self.hbox.addWidget(self.NextLevelLabel, 1, 1)
        self.hbox.addWidget(self.PrincessWidget, 1, 1)
        self.hbox.addWidget(self.MarioWidget1, 1, 1)
        self.hbox.addWidget(self.MarioWidget2, 1, 1)
        self.hbox.addWidget(self.DonkeyWidget, 1, 1)
        self.hbox.addWidget(self.LivesWidget1, 1, 1)
        self.hbox.addWidget(self.LivesWidget2, 1, 1)
        self.hbox.addWidget(self.PowerUpWidget, 1, 1)
        for i in range(0, 15):
            self.hbox.addWidget(self.barrels[i], 1, 1)

    def initialize_pipes(self):
        self.ex_pipe, self.in_pipe = mp.Pipe()
        self.player1_pipe, self.player2_pipe = mp.Pipe()
        self.player_pipe, self.power_up_pipe = mp.Pipe()
        self.player_donkey_pipe, self.donkey_player_pipe = mp.Pipe()
        self.player1_movement_pipe, self.movement_player1_pipe = mp.Pipe()
        self.player2_movement_pipe, self.movement_player2_pipe = mp.Pipe()

    def showHideWdigets(self):
        oImage = QImage("Images/dk1.png")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.hbox.addWidget(self.exitButton, 8, 5)
        self.exitButton.show()
        self.hbox.addWidget(self.startButton, 8, 3)
        self.startButton.show()
        self.hbox.addWidget(self.onlineButton, 8, 1)
        self.onlineButton.show()
        self.menuButton.hide()
        self.scoreLabelText.hide()
        self.scoreLabelText2.hide()
        self.scoreLabelMover1.hide()
        self.scoreLabelMover2.hide()
        self.scoreLabelResult.hide()

    def initialize_level_and_lives(self):
        self.scoreLabel1 = Score(self.ScoreLabel1)
        self.scoreLabel2 = Score(self.ScoreLabel2)
        self.scoreLabel1.setGeometry(19, 48, 100, 38)
        self.scoreLabel2.setGeometry(450, 48, 100, 38)
        self.levelLabel = Level(self.LevelLabel)
        self.levelLabel.setGeometry(274, -8, 100, 70)
        self.next_level = Level(self.NextLevelLabel)
        self.next_level.setGeometry(160, 200, 300, 300)
        self.next_level.setText("")
        self.livesWidget1 = Lives(self.LivesWidget1)
        self.livesWidget2 = Lives(self.LivesWidget2)
        self.livesWidget1.setGeometry(9, 4, 100, 70)
        self.livesWidget2.setGeometry(440, 4, 100, 70)

    def on_start(self):
        self.game_started = True
        self.online_game = False

        oImage = QImage("Images/Background2.png")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.startButton.hide()
        self.exitButton.hide()
        self.onlineButton.hide()

        self.initialize()
        self.initialize_pipes()
        self.initialize_level_and_lives()

        self.powerUp = PowerUp(self.in_pipe, self.power_up_pipe, self.my_obj_rwlock, self.PowerUpWidget)
        self.donkey = DonkeyKong(self.in_pipe, self.donkey_player_pipe, self.my_obj_rwlock, None, self.DonkeyWidget)
        self.donkey_barrels = []
        for i in range(0, 15):
            self.donkey_barrels.append(Barrel(self.in_pipe, self.my_obj_rwlock, self.donkey, self.barrels[i]))
        self.mover1 = Mover(self.next_level, self.in_pipe, self.player1_pipe, self.player_pipe, self.player_donkey_pipe,
                            self.player1_movement_pipe, self.livesWidget1, self.levelLabel, self.scoreLabel1,
                            self.my_obj_rwlock, True, self.powerUp, self.PowerUpWidget, self.MarioWidget1)
        self.mover2 = Mover(self.next_level, self.in_pipe, self.player2_pipe, self.player_pipe, self.player_donkey_pipe,
                            self.player2_movement_pipe, self.livesWidget2, self.levelLabel, self.scoreLabel2,
                            self.my_obj_rwlock, False, self.powerUp, self.PowerUpWidget, self.MarioWidget2)
        self.princess = Princess(self.PrincessWidget)

        self.map_process = Map.GameMap(self.ex_pipe, max_arg=101)
        self.map_process.start()

        self.queue = mp.Queue()
        self.movement_process = Movement.MovementProcess(self.movement_player1_pipe, self.movement_player2_pipe,
                                                         self.queue, None, max_arg=101)
        self.movement_process.start()

        self.th = Thread(target=self.check_for_game_end, args=())
        self.th.do_run = True
        self.th.start()

        self.hbox.update()

    def keyPressEvent(self, event):
        if self.game_started:
            if event.key() == Qt.Key_W:
                self.queue.put("W")
            elif event.key() == Qt.Key_A:
                self.queue.put("A")
            elif event.key() == Qt.Key_S:
                self.queue.put("S")
            elif event.key() == Qt.Key_D:
                self.queue.put("D")
            elif event.key() == Qt.Key_I:
                self.queue.put("I")
            elif event.key() == Qt.Key_J:
                self.queue.put("J")
            elif event.key() == Qt.Key_K:
                self.queue.put("K")
            elif event.key() == Qt.Key_L:
                self.queue.put("L")


        if event.key() == Qt.Key_R:
            self.princess.kill = True
            self.donkey.kill = True
            self.powerUp.kill = True
            self.PrincessWidget.hide()
            self.MarioWidget1.hide()
            self.MarioWidget2.hide()
            self.DonkeyWidget.hide()
            self.LivesWidget1.hide()
            self.ScoreLabel1.hide()
            self.LivesWidget2.hide()
            self.ScoreLabel2.hide()
            self.LevelLabel.hide()
            self.PowerUpWidget.hide()
            for i in range(0, 15):
                self.barrels[i].hide()

            for i in range(0, 15):
                self.layout().removeWidget(self.barrels[i])

            self.resultInfo()

    def check_for_game_end(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
           if self.mover1.lives == 0 and self.mover2.lives == 0:
               print("over")
               t.do_run = False
               '''for i in reversed(range(self.hbox.count())):
                   widgetToRemove = self.hbox.itemAt(i).widget()
                   self.hbox.removeWidget(widgetToRemove)
                   widgetToRemove.setParent(None)
               self.resultInfo()
               #self.hbox.update()'''
               self.princess.kill = True
               self.donkey.kill = True
               self.powerUp.kill = True
               self.mover1.kill = True
               self.mover2.kill = True
               if not self.online_game:
                   self.map_process.kill = True
                   self.movement_process.kill = True
               self.PrincessWidget.hide()
               self.MarioWidget1.hide()
               self.MarioWidget2.hide()
               self.DonkeyWidget.hide()
               self.LivesWidget1.hide()
               self.ScoreLabel1.hide()
               self.LivesWidget2.hide()
               self.ScoreLabel2.hide()
               self.LevelLabel.hide()
               self.PowerUpWidget.hide()
               for i in range(0, 15):
                   self.barrels[i].hide()

               for i in range(0, 15):
                   self.layout().removeWidget(self.barrels[i])

               self.scoreLabelText.show()
               self.scoreLabelText2.show()
               self.scoreLabelMover1.show()
               self.scoreLabelMover2.show()
               self.scoreLabelResult.show()

               self.resultInfo()

           time.sleep(0.5)

    def resultInfo(self):
        self.game_started = False
        self.firstTime = False
        self.online_game = False

        oImage = QImage("Images/black.jpg")
        sImage = oImage.scaled(QSize(600, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.hbox.addWidget(self.menuButton,10,10)
        self.menuButton.show()

        # self.ScoreLabelText = QLabel("Score: 0", self)
        self.hbox.addWidget(self.ScoreLabelText, 1, 1)
        #self.scoreLabelText = Score(self.ScoreLabelText)
        #self.scoreLabelText.setGeometry(70, 278, 100, 18)
        #self.scoreLabelText.text(1)
        self.ScoreLabelText.show()

        #self.ScoreLabelText2 = QLabel("Score: 0", self)
        self.hbox.addWidget(self.ScoreLabelText2, 1, 1)
        #self.scoreLabelText2 = Score(self.ScoreLabelText2)
        #self.scoreLabelText2.setGeometry(370, 278, 100, 18)
        #self.scoreLabelText2.text(2)
        self.ScoreLabelText2.show()

        #self.ScoreLabelMover1 = QLabel("Score: 0", self)
        self.hbox.addWidget(self.ScoreLabelMover1, 1, 1)
        #self.scoreLabelMover1 = Score(self.ScoreLabelMover1)
        #self.scoreLabelMover1.setGeometry(120, 348, 100, 38)
        self.scoreLabelMover1.setText(format(str(self.mover1.score)))
        self.ScoreLabelMover1.show()

        #self.ScoreLabelMover2 = QLabel("Score: 0", self)
        self.hbox.addWidget(self.ScoreLabelMover2, 1, 1)
        #self.scoreLabelMover2 = Score(self.ScoreLabelMover2)
        #self.scoreLabelMover2.setGeometry(420, 348, 100, 38)
        self.scoreLabelMover2.setText(format(str(self.mover2.score)))
        self.ScoreLabelMover2.show()

        #self.ScoreLabelResult = QLabel("Score: 0", self)
        self.hbox.addWidget(self.ScoreLabelResult, 1, 1)
        #self.scoreLabelResult = Score(self.ScoreLabelResult)
        #self.scoreLabelResult.setGeometry(210, 148, 300, 38)
        #self.scoreLabelResult.setStyleSheet("background-color: black; color: red; font-size:18px; font: bold System")
        if(self.mover1.score>self.mover2.score):
            self.scoreLabelResult.setText("PLAYER 1 WON")
        elif(self.mover1.score<self.mover2.score):
            self.scoreLabelResult.setText("PLAYER 2 WON")
        else:
            self.scoreLabelResult.setText("NO WINNER")
        self.ScoreLabelResult.show()
        self.hbox.update()
        #self.setLayout(self.hbox)
        #self.setGeometry(400, 35, 600, 700)
        #self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
