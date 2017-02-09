# -*- coding: utf-8 -*-


import socket
import threading

class Receiver(threading.Thread):

    def __init__(self, port, max_part):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket()
        self.data = ''
        self.part = 0
        self.max_part = max_part

    def run(self):
        self.sock.connect(('127.0.0.1', self.port))

        while True:
            self.part = self.sock.recv(2)
            if self.part == 'KO':
                break
            print CASHE + self.part + '.mpg'
            f = open(CASHE + self.part + '.mpg', 'wb')
            while self.data != 'p-end' and not 'p-end' in self.data:
                self.data = self.sock.recv(1024)
                f.write(self.data)
            self.data = ''
            self.sock.send('next')


class Communication():

    def __init__(self, sock):
        self.sock = sock

    def handle_message(self, data):
        if data[:3] == 'ok:':
            port = int(data[3:7])
            parts = int(data[8:])
            receive = Receiver(port, parts)
            receive.start()





IP, PORT = '127.0.0.1', 7777
CASHE = "E:\\tmp\\here\\"





sock = socket.socket()
sock.connect((IP, PORT))

com = Communication(sock)

sock.send('Watch:' + 'Movie Name')
data = sock.recv(1024)
com.handle_message(data)


sock.close()