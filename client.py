# -*- coding: utf-8 -*-


import socket
import threading
import pygame
from os import listdir
from os.path import isfile, join
import time
import sys
import hashlib

class Receiver(threading.Thread):
    """thread that receives video stream and saves it"""

    def __init__(self, port, max_part):
        """constractor: builds a receiver thread"""
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket()
        self.data = ''
        self.part = 0
        self.max_part = max_part

    def run(self):
        """gets the stream and saves it in the cashe"""
        self.sock.connect((IP, self.port))

        while True:
            self.part = self.sock.recv(3)
            if self.part == 'END':
                break
            print CASHE + self.part + '.mpg'
            f = open(CASHE + self.part + '.mpg', 'wb')
            while self.data != 'p-end' and not 'p-end' in self.data:
                self.data = self.sock.recv(1024)
                f.write(self.data)
            self.data = ''
            self.sock.send('next')


class Uploader(threading.Thread):
    """thread that uploads a file to the server"""

    def __init__(self, port, path):
        """constractor: builds an uploader thread"""
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket()
        self.path = path
        self.data = ''

    def run(self):
        """uploads a file to the server"""
        m = hashlib.md5
        self.sock.connect((IP, self.port))
        f = open(self.path, 'rb')
        dat = f.read(4096)
        print 'uploading...'
        while dat != '':
            hashed = m(dat)
            self.sock.send(hashed.hexdigest())
            self.data = self.sock.recv(2)

            if not self.data == 'ok':
                return

            self.sock.send(dat)
            self.data = self.sock.recv(2)
            while self.data == 'sa':
                self.sock.send(dat)
                self.data = self.sock.recv(2)
            if self.data == 'kg':
                dat = f.read(4096)
            else:
                return

        f.close()
        self.sock.send('end-of-upload')
        self.data = self.sock.recv(1024)
        if self.data == 'complete':
            self.sock.close()
        else:
            pass




class Communication():

    def __init__(self, sock):
        self.sock = sock

    def handle_message(self, data):
        print data
        if data[:13] == 'video_stream:':
            port = int(data[13:17])
            parts = int(data[18:])
            receive = Receiver(port, parts)
            receive.start()
        elif data[:16] == 'upload_approved:':
            port = int(data[16:])
            uploader = Uploader(port, upload_path)
            uploader.start()



def get_part_video_num(num):
    if len(str(num)) == 1:
        return '00' + str(num)
    elif len(str(num)) == 2:
        return '0' + str(num)
    else:
        return str(num)



def generate_file_md5(filename, blocksize=2**20):
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()





IP, PORT = '127.0.0.1', 7777
CASHE = "D:\\here2\\"
#CASHE = "E:\\tmp\\here\\"





sock = socket.socket()
sock.connect((IP, PORT))

com = Communication(sock)


if 1 == 2:
    sock.send('Watch:' + 'Movie Name')
    data = sock.recv(1024)
    com.handle_message(data)


    FPS = 30

    incashe = [f for f in listdir('D:\\here2\\') if isfile(join('E:\\tmp\\here', f))]
    t = time.time()

    while not isfile("D:\\here2\\000.mpg") or len(incashe) < 5:
        incashe = [f for f in listdir('D:\\here2') if isfile(join('D:\\here2', f))]
        if time.time() - t > 15:
            break

    else:
        print len(incashe)
        print 've hhazozrot'
        print not isfile("D:\\here2\\000.mpg")

        pygame.init()
        clock = pygame.time.Clock()
        movie = pygame.movie.Movie("D:\\here2\\000.mpg")
        screen = pygame.display.set_mode(movie.get_size())
        #movie_screen = pygame.Surface(movie.get_size()).convert
        movie_screen = pygame.display.set_mode((1024, 768))
        pygame.display.flip()

        movie.set_display(movie_screen, [0, 0, 352, 240])
        #movie.set_display(movie_screen, [0, 0, 528, 360])
        movie.play()

        num = 1
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    movie.stop()
                    playing = False

            if not movie.get_busy() and playing:
                print num
                movie = pygame.movie.Movie("D:\\here2\\" + get_part_video_num(num) + '.mpg')
                movie.set_display(movie_screen)
                movie.play()
                num += 1

            screen.blit(movie_screen, (0, 0))
            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()


    sock.close()

if 1 == 1:
    #upload_path = "E:\\tmp\\WTF.mp4"
    upload_path = "D:\\The_Hobbit_Trailer.mp4"
    #upload_path = "D:\\dogs.mp4"
    file_hash = generate_file_md5(upload_path)
    sock.send('upload:' + 'testname:!:' + file_hash)
    data = sock.recv(1024)
    com.handle_message(data)