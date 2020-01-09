import socket
import multiprocessing as mp

from PyQt5.QtWidgets import QWidget

import ServerMap
import ServerMovement
from DonkeyKongServer import DonkeyKongServer
from PowerUpServer import PowerUpServer

HOST = ''
PORT = 50005


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

    while True:
        end_queue = mp.Queue()
        count = 0
        s.listen(2)
        conns = []
        addrs = []
        print('Server is ready for new connections...')
        while count < 2:
            conn, addr = s.accept()
            conns.append(conn)
            addrs.append(addr)
            count += 1

            print('Connected by', addr)

        for i in range(0, 2):
            text2send = "Player"
            text2send += " " + str(i+1)
            conns[i].sendall(text2send.encode('utf8'))

        movement_queue = mp.Queue()
        movement_process1 = ServerMovement.ServerMovementProcess(movement_queue, conns[0], True, end_queue, max_arg=101)
        movement_process1.start()
        movement_process2 = ServerMovement.ServerMovementProcess(movement_queue, conns[1], False, end_queue, max_arg=101)
        movement_process2.start()

        in_pipe1, ex_pipe1 = mp.Pipe()
        in_pipe2, ex_pipe2 = mp.Pipe()
        donkey = DonkeyKongServer(movement_queue, ex_pipe1)
        powerUp = PowerUpServer(movement_queue, ex_pipe2)

        map_process = ServerMap.GameMap(movement_queue, conns, in_pipe1, in_pipe2, end_queue, max_arg=101)
        map_process.start()

        end_queue.get()
        donkey.kill = True
        powerUp.kill = True
