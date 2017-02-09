# -*- coding: utf-8 -*-


import socket
import select
import threading
from random import randint


class Streamer(threading.Thread):

    def __init__(self, thread_id, port, filePath, part, numOfParts):
        """constractor: create a video streamer thread"""
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.port = port
        self.sock = socket.socket()
        self.client = None
        self.address = None
        self.file = None
        self.filePath = filePath
        self.part = part
        self.numOfParts = numOfParts

    def run(self):
        """streams a video to a single client"""
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen(1)
        (self.client, self.address) = self.sock.accept()

        while self.part < self.numOfParts:
            self.file = open(self.filePath + str(self.part) + '.mpg', 'rb')
            #self.sock.send('part' + str(self.part) + ':' + fileraw)
            print self.part
            if len(str(self.part)) == 1:
                self.client.send('0' + str(self.part))
            else:
                self.client.send(str(self.part))
            fileraw = self.file.read(1024)
            while fileraw != '':
                self.client.send(fileraw)
                fileraw = self.file.read(1024)
            self.client.send('p-end')
            ok = self.client.recv(4)
            self.part += 1
            self.check_request()
            self.file.close()

        self.client.send('KO')
        self.sock.close()

    def check_request(self):
        """checks if a client request was made"""
        pass




class Communication():
    """handles the communication of the server"""

    def __init__(self, sock):
        """gets the servers socket"""
        self.sock = sock

    def handle_request(self, dat, client):
        """handles the data and returns the requested action"""
        if dat == "" or dat == "exit":
            open_client_sockets.remove(client)
            print "Connection with client closed"
        elif dat[:6] == 'Watch:':
            #stream = Streamer(0, randint(3000, 7777), '', 0, 10)
            name = dat[6:]
            fold, parts = sql.get_movie(name)
            port = randint(3000, 7000)

            #mutex.acquire()
            #threads[port] = 'ok'
            #mutex.release()

            stream = Streamer(0, port, fold, 0, parts)
            #stream = Streamer(0, 5555, "D:\\dum_dogs\\gt", 0, 30)
            stream.start()
            self.send_to_customer('ok:' + str(port) + ':' + str(parts), client)

    def send_to_customer(self, dat, client):
        """sends to the client the data"""
        client.send(dat)


class Sqlcommands():
    """a class that handles the communication with the database"""

    def __init__(self):
        """gets the sql database"""
        pass

    def get_movie(self, name):
        return PATH, 10



PATH = "E:\\tmp\\test_subj\\"


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 7777))
server_socket.listen(10)
open_client_sockets = []
#numOfThreads = 0

threads = {}
#will be the ipc controller
mutex = threading.Lock()

#handles the requests
com = Communication(server_socket)
#handles database
sql = Sqlcommands()


while True:
    rlist, wlist, xlist = select.select([server_socket]+open_client_sockets, [], [])

    #itarates over all of the requests
    for current_socket in rlist:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_sockets.append(new_socket)
        else:
            data = current_socket.recv(1024)

            com.handle_request(data, current_socket)
