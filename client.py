# -*- coding: utf-8 -*-


import socket
import threading
import pygame
from os import listdir
from os.path import isfile, join
import time
import sys

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


class Communication():

    def __init__(self, sock):
        self.sock = sock

    def handle_message(self, data):
        if data[:3] == 'ok:':
            port = int(data[3:7])
            parts = int(data[8:])
            receive = Receiver(port, parts)
            receive.start()



def get_part_video_num(num):
    if len(str(num)) == 1:
        return '00' + str(num)
    elif len(str(num)) == 2:
        return '0' + str(num)
    else:
        return str(num)





IP, PORT = '127.0.0.1', 7777
#CASHE = "D:\\here2\\"
CASHE = "E:\\tmp\\here\\"





sock = socket.socket()
sock.connect((IP, PORT))

com = Communication(sock)



sock.send('Watch:' + 'Movie Name')
data = sock.recv(1024)
com.handle_message(data)


FPS = 30

incashe = [f for f in listdir('E:\\tmp\\here') if isfile(join('E:\\tmp\\here', f))]
t = time.time()

while not isfile("E:\\tmp\\here\\000.mpg") or len(incashe) < 5:
    incashe = [f for f in listdir('E:\\tmp\\here') if isfile(join('E:\\tmp\\here', f))]
    if time.time() - t > 15:
        break

else:
    print len(incashe)
    print 've hhazozrot'
    print not isfile("E:\\tmp\\here\\000.mpg")

    pygame.init()
    clock = pygame.time.Clock()
    movie = pygame.movie.Movie("E:\\tmp\\here\\000.mpg")
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
            movie = pygame.movie.Movie("E:\\tmp\\here\\" + get_part_video_num(num) + '.mpg')
            movie.set_display(movie_screen)
            movie.play()
            num += 1

        screen.blit(movie_screen, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


sock.close()