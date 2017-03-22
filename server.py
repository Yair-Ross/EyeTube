# -*- coding: utf-8 -*-


import socket
import select
import threading
from random import randint
import sqlite3
import hashlib
import os
import video_manager
from subprocess import call
import sys


class Streamer(threading.Thread):
    """streams the video to the client"""

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
            self.file = open(self.filePath + self.get_part_video_num() + '.mpg', 'rb')
            print self.get_part_video_num()
            #sends the part number to the client
            self.client.send(self.get_part_video_num())

            fileraw = self.file.read(1024)
            #video part
            while fileraw != '':
                self.client.send(fileraw)
                fileraw = self.file.read(1024)
            self.client.send('v-end')
            ok = self.client.recv(4)
            self.file.close()

            self.file = open(self.filePath + self.get_part_video_num() + '.wav', 'rb')
            fileraw = self.file.read(1024)
            #video part
            while fileraw != '':
                self.client.send(fileraw)
                fileraw = self.file.read(1024)
            self.client.send('w-end')
            ok = self.client.recv(4)
            self.file.close()

            self.part += 1
            #if client want to exit or skip to part it gets it here
            self.check_request()

        self.stop()

    def get_part_video_num(self):
        """gets a number (between 0 to 999) and converts it into a 3 digit string"""
        if len(str(self.part)) == 1:
            return '00' + str(self.part)
        elif len(str(self.part)) == 2:
            return '0' + str(self.part)
        else:
            return str(self.part)


    def check_request(self):
        """checks if a client request was made"""
        mutex.acquire()
        cond = threads[self.port]
        mutex.release()

        #nothing new
        if cond[0] == 0:
            pass
        else:
            #send from part
            if cond[0] == 1:
                pass
            #terminate\stop
            elif cond[0] == 2:
                pass
            #send parts
            elif cond[0] == 3:
                pass

            #deletes to normal condition
            mutex.acquire()
            threads[self.port] = (0, 0)
            mutex.release()

    def change_part(self, partnum):
        """change the parts from wich it will send"""
        if partnum.isdigit() and int(partnum) < self.numOfParts:
            self.part = partnum

    def stop(self):
        """stops the server thread"""
        self.client.send('END')
        self.client.close()
        self.sock.close()
        #removes from thread dict
        mutex.acquire()
        threads.pop(self.port)
        mutex.release()


    def send_parts(self):
        """sends parts in list"""
        pass




class Receive_vid(threading.Thread):
    """receive upload of a video"""

    def __init__(self, port, temp_path, name, hashfile):
        """constractor: create a video upload receiver thread"""
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket()
        self.temp_path = temp_path
        self.count = 0
        self.data = ''
        self.name = name
        self.hashfile = hashfile

    def run(self):
        """starts a receiver thread"""
        m = hashlib.md5
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen(1)
        (self.client, self.address) = self.sock.accept()

        f = open(self.temp_path, 'wb')

        while True:
            c_hash = self.client.recv(32)
            #if upload has ended
            if c_hash == 'end-of-upload-d-o-n-e-now-what-?':
                f.close()
                #creates a new foulder for the video
                if not os.path.exists(PATH+self.name):
                    os.makedirs(PATH+self.name)

                vid = video_manager.Video_manager(path=self.temp_path, split_path=PATH+self.name+'\\')
                #converts video to valid format
                vid.divide_video()

                self.client.send('complete')
                self.client.close()
                self.sock.close()

                #database insert will be here
                mutex.acquire()
                threads[self.port] = (self.name, PATH+self.name+'\\', vid.get_length(), self.hashfile, vid.get_num_of_parts(), vid.get_size())
                mutex.release()

                os.remove(self.temp_path)

                break
            #sends the client to send data
            self.client.send('ok')
            #note: receiving more than 1024 is buggy and sometimes data gets cut and is received in next receive
            self.data = self.client.recv(1024)
            hashed = m(self.data)
            #in case data came not as it supposed to
            while not hashed.hexdigest() == c_hash:
                self.count += 1
                #after 10 times the upload is cancelled
                if self.count > 10:
                    self.client.close()
                    f.close()
                    #deletes the file
                    os.remove(self.temp_path)
                    return
                self.client.send('sa')
                c_hash = self.client.recv(32)
                self.client.send('ok')
                self.data = self.client.recv(1024)
                hashed = m(self.data)
            else:
                #tells the client to keep sending
                self.client.send('kg')
                f.write(self.data)
                self.count == 0







class Communication():
    """handles the communication of the server"""

    def __init__(self, sock):
        """gets the servers socket"""
        self.sock = sock

    def handle_request(self, dat, client):
        """handles the data and returns the requested action"""
        print dat
        if dat == "" or dat == "exit":
            #client disconnected
            open_client_sockets.remove(client)
            print "Connection with client closed"

        elif dat[:6] == 'parts:':
            name = dat[6:]
            if sql.exists_in_base('MOVIE_NAME', name):
                fold, parts = sql.get_movie(name)
                self.send_to_customer('parts:' + str(parts), client)
            else:
                self.send_to_customer('vid_not_found', client)


        elif dat[:7] == 'search:':
            #searches video
            serch_word = dat[7:]
            results = sql.return_search_results(serch_word)
            results = sorted(results, key=lambda results: results[1])[::-1]
            for i in results:
                if i[0] == serch_word:
                    results.remove(i)
                    results = [i] + results
                    break

            self.send_to_customer('start results:', client)
            for search_dat in results:
                self.send_to_customer('res:' + search_dat[0] + ':!:' + search_dat[1] + ':!:' + search_dat[2], client)
            self.send_to_customer('end results:', client)


        elif dat[:6] == 'Watch:':
            #in this case the client want to watch a video
            name = dat[6:]
            if sql.exists_in_base('MOVIE_NAME', name):
                fold, parts = sql.get_movie(name)
                port = rand_port()

                mutex.acquire()
                threads[port] = (0, 0)
                mutex.release()

                stream = Streamer(0, port, fold, 0, parts)
                stream.start()
                self.send_to_customer('video_stream:' + str(port) + ':' + str(parts), client)
            else:
                self.send_to_customer('vid_not_found', client)

        elif dat[:5] == 'from:':
            #in this case the client wanted to skip to a certain part of a video
            port = dat[5:9]
            part = dat[10:]
            mutex.acquire()
            #prevents the creation of "dead" ports by the client
            if port in threads:
                threads[port] = (1, part)
            mutex.release()

        elif dat[:5] == 'stop:':
            #client no longer want to watch the movie
            port = dat[5:]
            mutex.acquire()
            #prevents the creation of "dead" ports by the client
            if port in threads:
                threads[port] = (2, 0)
            mutex.release()

        elif dat[:7] == 'upload:':
            #in this case client wants to upload a file
            name = dat[7:dat.index(':!:')]
            f_hash = dat[dat.index(':!:') + 3:]
            if not sql.exists_in_base('HASH', f_hash) and not sql.exists_in_base('MOVIE_NAME', name):
                port = rand_port()

                mutex.acquire()
                threads[port] = (0, 0)
                mutex.release()

                receiver = Receive_vid(port, TMP_UPLOAD + 'tmp_' + name + str(port) + '.mp4', name, f_hash)
                receiver.start()

                self.send_to_customer('upload_approved:' + str(port), client)
            else:
                self.send_to_customer('invalid', client)



    def send_to_customer(self, dat, client):
        """sends to the client the data"""
        client.send(dat)


class Sqlcommands():
    """a class that handles the communication with the database"""

    def __init__(self, base):
        """gets the sql database"""
        self.conn = sqlite3.connect(base)
        """if not self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='spwords'").fetchone():
            self.conn.execute('''CREATE TABLE VIDEOS
                   (ID INT PRIMARY KEY     NOT NULL,
                   MOVIE_NAME     TEXT    NOT NULL,
                   MOVIE_PATH     TEXT    NOT NULL,
                   LEN            INT     NOT NULL,
                   VIEWS          INT     NOT NULL,
                   SCORE          REAL,
                   HASH           TEXT    NOT NULL,
                   PARTS          INT     NOT NULL,
                   SIZE         REAL);''')"""

    def get_movie(self, name):
        """returns the movie path and number of parts"""
        inf = self.conn.execute("SELECT MOVIE_PATH, PARTS FROM VIDEOS WHERE MOVIE_NAME='%s'" % (name)).fetchone()
        if inf:
            return str(inf[0]), inf[1]

    def exists_in_base(self, param, value):
        """returns if exists in database"""
        a = self.conn.execute("SELECT EXISTS(SELECT 1 FROM VIDEOS WHERE %s='%s')" % (param, value)).fetchone()

        if a[0] != 0:
            return True
        else:
            return False

    def add_movie(self, id, name, path, len, views, score, hashf, parts, size):
        """adds a movie data to videos table in database"""
        name = "'" + name + "'"
        path = "'" + path + "'"
        hashf = "'" + hashf + "'"
        self.conn.execute("INSERT INTO VIDEOS (ID,MOVIE_NAME,MOVIE_PATH,LEN,VIEWS,SCORE,HASH,PARTS,SIZE) \
              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (id, name, path, len, views, score, hashf, parts, size));

        self.conn.commit()

    def return_search_results(self, name):
        """returns the results of a search"""
        cursor = self.conn.execute("SELECT ID, MOVIE_NAME, VIEWS, SCORE  from VIDEOS")

        return [(str(row[1]), row[2], row[3]) for row in cursor if name in str(row[1])]

    def get_max_id(self):
        """returns the max id in the table"""
        return self.conn.execute("SELECT max(ID) FROM VIDEOS").fetchone()[0]


def rand_port():
    """returns a random port which isn't used already"""
    p = randint(3000, 7000)
    while True:
        mutex.acquire()
        l = threads
        mutex.release()
        if p in l:
            p = randint(3000, 7000)
        else:
            break
    return p



try:
    call('ffmpeg -version')
except:
    #in case ffmpeg is not installed
    print 'YOU NEED TO INSTALL FFMPEG TO RUN THIS SERVER!'
    os._exit(0)


if len(sys.argv) < 2:
    print 'you need to enter an empty folder to save the videos'
    sys.exit()



PATH = sys.argv[1]
TMP_UPLOAD = sys.argv[1]

#PATH = "D:\\"
#PATH = "D:\\testname\\testname\\"
#PATH = "E:\\tmp\\vids\\"
#TMP_UPLOAD = 'E:\\tmp\\upload_tmp\\'
#TMP_UPLOAD = "D:\\server_data\\"
#PATH = "E:\\tmp\\test_subj\\"
#PATH = "E:\\tmp\\"


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 7777))
server_socket.listen(10)
open_client_sockets = []

#will be a dictionary that will be built from a port key and a request tuple
threads = {}
#will be the ipc controller
mutex = threading.Lock()

#handles the requests
com = Communication(server_socket)
#handles database
sql = Sqlcommands("e:\\vids.db")

#main server loop
while True:
    rlist, wlist, xlist = select.select([server_socket]+open_client_sockets, [], [], 0)

    #itarates over all of the requests
    for current_socket in rlist:
        #checks if a new socked connects
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_sockets.append(new_socket)
        else:
            #gets the data
            data = current_socket.recv(1024)
            #handles the client request
            com.handle_request(data, current_socket)

    if len(threads) > 0:

        mutex.acquire()
        #copies the thread list so that the other threads wont wait for too long
        dup_threads = threads.copy()
        mutex.release()

        for port, values in dup_threads.iteritems():
            if len(values) > 5:
                vid_id = sql.get_max_id()
                if vid_id:
                    vid_id += 1
                else:
                    vid_id = 1
                sql.add_movie(vid_id, values[0], values[1], values[2], 0, 0, values[3], values[4], values[5])

                #earazes the thread from the dictionary thus it ended its work
                mutex.acquire()
                threads.pop(port)
                mutex.release()