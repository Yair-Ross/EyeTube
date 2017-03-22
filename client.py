# -*- coding: utf-8 -*-


import socket
import threading
import pygame
from os import listdir
from os.path import isfile, join
from os.path import exists
from os import makedirs
import time
import sys
import hashlib
import pyaudio
import wave

class Receiver(threading.Thread):
    """thread that receives video stream and saves it"""

    def __init__(self, port, max_part, cashe):
        """constractor: builds a receiver thread"""
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket()
        self.data = ''
        self.part = 0
        self.max_part = max_part
        self.cashe = cashe

    def run(self):
        """gets the stream and saves it in the cashe"""
        self.sock.connect((IP, self.port))

        while True:
            #gets a num of part (the video and the audio)
            self.part = self.sock.recv(3)
            #in case the video has ended
            if self.part == 'END':
                self.sock.close()
                print 'wah'
                #ends the thread
                return
            print self.cashe + self.part + '.mpg'
            #video part
            f = open(self.cashe + self.part + '.mpg', 'wb')
            #sometime v-end (tells the part ended) comes connected to the file data
            while self.data != 'v-end' and not 'v-end' in self.data:
                self.data = self.sock.recv(1024)
                f.write(self.data)
            f.close()
            #sends to streamer to start audio part stream
            self.sock.send('sond')
            #audio part
            f = open(self.cashe + self.part + '.wav', 'wb')
            #just like in the video part sometime w-end (tells the part ended) comes connected to the file data
            while self.data != 'w-end' and not 'w-end' in self.data:
                self.data = self.sock.recv(1024)
                f.write(self.data)

            f.close()
            self.data = ''
            #tells that next part can be send
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
        #the uploaded file
        f = open(self.path, 'rb')
        dat = f.read(1024)
        print 'uploading...'
        while dat != '':
            hashed = m(dat)
            self.sock.send(hashed.hexdigest())
            self.data = self.sock.recv(2)

            if not self.data == 'ok':
                #somthing went wrong and the thread instantly stops
                return

            self.sock.send(dat)
            self.data = self.sock.recv(2)
            #in case the data didn't and the hash sent didn't match
            while self.data == 'sa':
                #sends again the hash and data
                hashed = m(dat)
                self.sock.send(hashed.hexdigest())
                print hashed.hexdigest()
                self.data = self.sock.recv(2)
                print self.data
                self.sock.send(dat)
                #print dat
                self.data = self.sock.recv(2)
            #can keep sending
            if self.data == 'kg':
                dat = f.read(1024)
            else:
                return

        f.close()
        self.sock.send('end-of-upload-d-o-n-e-now-what-?')
        print 'processing video... this may take a few minutes'
        self.data = self.sock.recv(1024)
        if self.data == 'complete':
            self.sock.close()
            uploading.set()
        else:
            pass


class Music_player(threading.Thread):
    """audio player thread object"""

    def __init__(self, part):
        """initilize thread"""
        threading.Thread.__init__(self)
        self.part = part
        self.next = False
        self.streamnum = 1


    def run(self):
        """runs audio of the video"""

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        musicdata = wf.readframes(CHUNK)

        while playing:
            if self.streamnum == 1:
                stream.write(musicdata)
                musicdata = wf.readframes(CHUNK)
            else:
                stream.write(musicdata)
                musicdata = wf2.readframes(CHUNK)
            if len(musicdata) < CHUNK or musicdata == '':
                if self.streamnum == 1:
                    self.streamnum = 2
                else:
                    self.streamnum = 1
                self.next = False

        stream.stop_stream()
        stream.close()

        p.terminate()


class Graphic_Ui():
    """a class that is responsible for the gui's paintings"""

    def __init__(self, bar_length, bar_high, bar_color, watch_color, loading_color, x, y):
        self.bar_length = bar_length
        self.bar_high = bar_high
        self.bar_color = bar_color
        self.watch_color = watch_color
        self.loading_color = loading_color
        self.x = x
        self.y = y
        self.bar = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.bar_length, self.bar_high))

    def show_video_bar(self, loading_num, viewed_num, total_num):
        pygame.draw.rect(screen, self.bar_color, (self.x + 1, self.y + 1, self.bar_length - 2, self.bar_high - 2))
        pygame.draw.rect(screen, self.loading_color, (self.x + 1, self.y + 1, int((float(loading_num)/total_num) * (self.bar_length - 2)), self.bar_high - 2))
        pygame.draw.rect(screen, self.watch_color, (self.x + 1, self.y + 1, int((float(viewed_num)/total_num) * (self.bar_length - 2)), self.bar_high - 2))


class Cache():
    """a class that handles the cashe"""
    def __init__(self):
        self.cache = CASHE

    def in_cashe(self, name, parts):
        if exists(CASHE + name + '\\') and len([f for f in listdir(CASHE + name + '\\') if isfile(join(CASHE + name + '\\', f))]) == parts:
            return True
        else:
            return False


class Communication():
    """class for communication with the server"""

    def __init__(self, sock):
        self.sock = sock
        self.partnum = 0

    def handle_message(self, data):
        """gets a message that was received from the server"""
        print data
        #video stream starts
        if data[:13] == 'video_stream:':
            #port will be between 3000 to 7000
            port = int(data[13:17])
            self.partnum = int(data[18:])

            #creates a video file in cache
            if not exists(CASHE + movie_name + '\\'):
                makedirs(CASHE + movie_name + '\\')

            receive = Receiver(port, self.partnum, CASHE + movie_name + '\\')
            receive.start()
        #upload stream approved
        elif data[:16] == 'upload_approved:':
            port = int(data[16:])
            uploader = Uploader(port, upload_path)
            uploader.start()
        elif data[:6] == 'parts:':
            if data[6:].isdigit():
                self.partnum = int(data[6:])
        elif data == 'invalid':
            print 'invalid upload'
        elif data == 'vid_not_found':
            self.partnum = -1
            print 'could not watch vid'



def get_part_video_num(num):
    """gets a number (between 0 to 999) and converts it into a 3 digit string"""
    if len(str(num)) == 1:
        return '00' + str(num)
    elif len(str(num)) == 2:
        return '0' + str(num)
    else:
        return str(num)



def generate_file_md5(filename, blocksize=2**20):
    """returns a hash for the file"""
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def play_vid():
    pass


if len(sys.argv) < 2:
    print 'you need to enter an empty cache folder'
    sys.exit()


IP, PORT = '127.0.0.1', 7777
#CASHE = "D:\\here2\\"
#CASHE = "E:\\tmp\\here\\"
CASHE = sys.argv[1]
CHUNK = 1024
FPS = 30
playing = True
uploading = threading.Event()




sock = socket.socket()
#connect to main server
sock.connect((IP, PORT))

com = Communication(sock)
cach = Cache()

print 'client version 1'
movie_name = raw_input('please enter video name: ')
'''upload_path = raw_input('please enter a path to an mp4 video which you want to upload: ')
while not isfile(upload_path) or not upload_path[-4:] == '.mp4':
    upload_path = raw_input('please enter a valid mp4 path: ')


if 1 == 1:
    #upload_path = "E:\\tmp\\ep1.mp4"
    #upload_path = "E:\\tmp\\WTF.mp4"
    #upload_path = "E:\\tmp\\dogs.mp4"
    #upload_path = "D:\\The_Hobbit_Trailer.mp4"
    #upload_path = "D:\\allstar.mp4"
    #upload_path = "E:\\tmp\\cats.mp4"
    #upload_path = "D:\\dogs.mp4"
    file_hash = generate_file_md5(upload_path)
    sock.send('upload:' + movie_name + ':!:' + file_hash)
    data = sock.recv(1024)
    com.handle_message(data)

uploading.wait()
time.sleep(7)'''
if 1 == 1:

    sock.send('parts:' + movie_name)
    data = sock.recv(1024)
    com.handle_message(data)
    numpart = com.partnum
    
    if not cach.in_cashe(movie_name, numpart) and not numpart == -1:
        sock.send('Watch:' + movie_name)
        data = sock.recv(1024)
        com.handle_message(data)

    if numpart != -1:

        #gets all files in cache
        incashe = [f for f in listdir(CASHE + movie_name + '\\') if isfile(join(CASHE + movie_name + '\\', f))]
        t = time.time()

        #checks if enough parts went in
        while not isfile(CASHE + movie_name + '\\' + "000.mpg") or len(incashe) < 5:
            incashe = [f for f in listdir(CASHE + movie_name + '\\') if isfile(join(CASHE + movie_name + '\\', f))]
            #timeout for waiting is 15 minutes
            if time.time() - t > 15:
                break

        else:
            print len(incashe)
            print 've hhazozrot'
            print not isfile(CASHE + movie_name + '\\')

            print numpart
            num = 0
            wf = wave.open(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav', 'rb')
            wf2 = wave.open(CASHE + movie_name + '\\' + get_part_video_num(num + 1) + '.wav', 'rb')
            #audio player
            player = Music_player(num)

            pygame.init()
            #needed for controlling the fps
            clock = pygame.time.Clock()
            movie = pygame.movie.Movie(CASHE + movie_name + '\\' + get_part_video_num(num) + ".mpg")
            screen = pygame.display.set_mode(movie.get_size())
            #movie_screen = pygame.Surface(movie.get_size()).convert
            movie_screen = pygame.display.set_mode((528, 768))
            movie_screen.fill((255, 255, 255))
            pygame.display.flip()

            movie.set_display(movie_screen, [0, 0, 528, 360])

            vid_bar = Graphic_Ui(528, 8, (105, 105, 105), (102, 255, 51), (192, 192, 192), 0, 362)
            vid_bar.show_video_bar(numpart, num, numpart)

            #starts the audio
            player.start()
            #starts movie
            movie.play()

            num += 1

            playing = True
            while playing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        movie.stop()
                        #will stop the audio too
                        playing = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if vid_bar.bar.collidepoint(pos):
                            pass
                            movie.stop()
                            playing = False
                            while player.isAlive():
                                pass

                            num = int((float(pos[0])/(vid_bar.bar_length-2)) * numpart)
                            print num

                            wf = wave.open(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav', 'rb')
                            wf2 = wave.open(CASHE + movie_name + '\\' + get_part_video_num(num + 1) + '.wav', 'rb')
                            #audio player
                            player = Music_player(num)
                            player.start()
                            movie = pygame.movie.Movie(CASHE + movie_name + '\\' + get_part_video_num(num) + '.mpg')
                            movie.set_display(movie_screen, [0, 0, 528, 360])
                            movie.play()
                            num += 1

                            vid_bar.show_video_bar(numpart, num, numpart)

                            playing = True

                if not movie.get_busy() and playing and isfile(CASHE + movie_name + '\\' + get_part_video_num(num) + '.mpg') and isfile(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav'):
                    print num
                    #next video part
                    movie = pygame.movie.Movie(CASHE + movie_name + '\\' + get_part_video_num(num) + '.mpg')
                    movie.set_display(movie_screen, [0, 0, 528, 360])
                    movie.play()
                    num += 1

                    vid_bar.show_video_bar(numpart, num, numpart)

                if not player.next and playing and isfile(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav'):
                    if player.streamnum == 2:
                        wf = wave.open(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav', 'rb')
                    else:
                        wf2 = wave.open(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav', 'rb')
                    player.next = True

                screen.blit(movie_screen, (0, 0))
                pygame.display.update()
                clock.tick(FPS)

            pygame.quit()
            #sys.exit()

    sock.close()

