from multiprocessing import Process, Pipe, Queue
from threading import Thread
from RWLock import RWLock
import socket


class ServerMovementProcess(Process):
    def __init__(self, queue: Queue, socket, left: bool, end_queue: Queue, max_arg: int):
        super().__init__(target=self.__count__, args=(queue, socket, left, end_queue))

    def __count__(self, queue: Queue, socket, left, end_queue: Queue):
        self.queue = queue
        self.socket = socket
        self.left = left
        self.end_queue = end_queue
        self.kill = False
        self.daemon = True
        self.th = Thread(target=self.check_end, args=())
        self.th.start()

        while not self.kill:
            self.movement = ''
            bin = self.socket.recv(1)
            self.movement += str(bin, 'utf-8')

            if left:
                if self.movement == "W" or self.movement == "A" or self.movement == "S" or self.movement == "D":
                    self.queue.put(self.movement)
            else:
                if self.movement == "I" or self.movement == "J" or self.movement == "K" or self.movement == "L":
                    self.queue.put(self.movement)

    def check_end(self):
        self.end_queue.get()
        self.kill = True
