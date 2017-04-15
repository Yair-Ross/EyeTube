# -*- coding: utf-8 -*-



import socket
import threading
import pygame
from os import listdir
from os.path import isfile, join
from os.path import exists, dirname, abspath
from os import makedirs, environ, chdir
import time
import sys
import hashlib
import pyaudio
import wave
import tkFileDialog
import tkMessageBox
import ttk
import video_manager

import Tkinter as tk
from tkFont import Font



class Receiver(threading.Thread):
    """thread that receives video stream and saves it"""

    def __init__(self, port, max_part, cashe):
        """constractor: builds a receiver thread"""
        threading.Thread.__init__(self)
        self.running = True
        self.port = port
        self.sock = socket.socket()
        self.data = ''
        self.part = 0
        self.max_part = max_part
        self.cashe = cashe

    def run(self):
        """gets the stream and saves it in the cache"""
        self.sock.connect((IP, self.port))

        while self.running:
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
        self.progress = 0
        self.sending = True

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
                self.progress += 1024
                dat = f.read(1024)
            else:
                return

            if not self.sending:

                self.sock.send('canceled')
                self.sock.close()
                f.close()
                return


        f.close()
        self.sock.send('end-of-upload-d-o-n-e-now-what-?')
        print 'processing video... this may take a few minutes'
        self.data = self.sock.recv(1024)
        if self.data == 'complete':
            self.sock.close()
            tasks.complete_upload()
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
        self.pause = False


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
            if self.pause:
                while True:
                    if not playing:
                        return
                    elif not self.pause:
                        break

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
        if exists(CASHE + name + '\\') and len([f for f in listdir(CASHE + name + '\\') if isfile(join(CASHE + name + '\\', f))])/2 == parts:
            return True
        else:
            return False


class Gui_handle():
    """activates gui events"""
    def __init__(self):
        self.kill = False
        self.mov_name = ''
        self.print_main = False
        self.print_upload = False
        self.upload_chosen = ''
        self.upload_canceled = False
        self.upload_complete = False
        self.back_from_upload = False
        #self.try_upload = False

    def close(self):
        self.kill = True

    def main_screen(self):
        self.print_main = True

    def upload_screen(self):
        self.print_upload = True

    def clear_upload(self):
        self.upload_canceled = True

    def complete_upload(self):
        self.upload_complete = True
        
    def out_of_upload(self):
        self.back_from_upload = True

    #def start_upload(self):
    #    self.try_upload = True


class Communication():
    """class for communication with the server"""

    def __init__(self, sock):
        self.sock = sock
        self.partnum = 0
        self.receive = ''
        self.res_list = []
        self.print_results = False
        self.uploader = None
        #this will inform the main program of the status of the uploading
        self.upload_num = 0

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

            self.receive = Receiver(port, self.partnum, CASHE + movie_name + '\\')
            self.receive.start()

        #upload stream approved
        elif data[:16] == 'upload_approved:':
            port = int(data[16:])
            self.uploader = Uploader(port, upload_path)
            self.uploader.start()
            self.upload_num = 1

        elif data[:6] == 'parts:':
            if data[6:].isdigit():
                self.partnum = int(data[6:])

        elif data[:8] == 'invalid:':
            self.uploader = None
            if data[8:] == 'hash':
                self.upload_num = 2
            else:
                self.upload_num = 3

            print 'invalid upload'

        elif data == 'vid_not_found':
            self.partnum = -1
            print 'could not watch vid'

        elif data[:8] == 'results:':
            results = data[8:].split(':<!>:')
            self.res_list = [['Movie Name', 'views', 'grade']]
            for i in results:
                datas = i.split(':!:')
                self.res_list.append(datas)
            self.print_results = True
            '''if results == ['']:
                self.print_results = False
            else:
                self.print_results = True'''



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


def update_bar_by_params(loader, viewed, maxed):
    """updates the bar by the parameters given"""
    if loader and loader.part.isdigit():
        loaded = int(loader.part)
    else:
        loaded = maxed
    vid_bar.show_video_bar(loaded, viewed, maxed)


def on_closing():
    '''if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()'''
    tasks.close()
    root.destroy()
    sys.exit()


def onsearch():
    name = entry.get()
    sock.send('search:' + name)
    data = sock.recv(1024)
    com.handle_message(data)


def onclick(x, y):
    #print com.res_list[y][0]
    tasks.mov_name = com.res_list[y][0]


def choosefile():
    """returns the path of the selected file"""

    # get filename
    filename = tkFileDialog.askopenfilename(**options)
    #print filename, '*****'

    # open file on your own
    if filename:
        #return open(filename, 'r')
        tasks.upload_chosen = filename


def on_upload():
    name = entry.get()
    if len(name) > 0:
        file_hash = generate_file_md5(upload_path)
        sock.send('upload:' + name + ':!:' + file_hash)
        data = sock.recv(1024)
        com.handle_message(data)
    else:
        com.upload_num = 7


def on_cancel():
    answer = tkMessageBox.askyesno("eyetube manager", "are you sure you want to cancel upload?")
    if the_sender and answer:
        the_sender.sending = False
        tasks.clear_upload()


def home_screen():
    pass


def play_vid():
    pass


if len(sys.argv) < 2:
    print 'you need to enter an empty cache folder'
    sys.exit()


#sets to current file directory
chdir(dirname(abspath(__file__)))

root = tk.Tk()
embed = tk.Frame(root, width=528, height=768)
embed.pack()

#results_frame = tk.Frame(embed, width=400, height=400)
#results_frame.place(in_=embed, anchor="c", relx=.50, rely=.50)

#tells the window to not chnge size
embed.pack_propagate(0)
#root.resizable(0,0)

# Tell pygame's SDL window which window ID to use
environ['SDL_WINDOWID'] = str(embed.winfo_id())

#setting some of the programs properties
root.wm_title("EyeTube")
root.iconbitmap("temp_illu.ico")
SCREEN_COLOR = 'dodger blue'
root.configure(background=SCREEN_COLOR)

# Show the window so it's assigned an ID.
root.update()

#text = tk.Button(root, text='stop', command=s.stopthat)
'''text = tk.Button(root, text='stop', width=20, command=on_closing)
text.pack(side='bottom')'''
#overrides the "X" button
root.protocol("WM_DELETE_WINDOW", on_closing)
tasks = Gui_handle()



IP, PORT = '127.0.0.1', 7777
#CASHE = "D:\\here2\\"
#CASHE = "E:\\tmp\\here\\"
movie = None

CASHE = sys.argv[1]

if not CASHE[-1] == '/' or not CASHE[-1] == '\\':
    CASHE += '\\'

CHUNK = 1024
FPS = 30
#playing = True
movie_name = ''


sock = socket.socket()
#connect to main server
sock.connect((IP, PORT))

com = Communication(sock)
cach = Cache()
'''
text = tk.Text(root, height=70, width=100)
text.pack(side=tk.BOTTOM)
text.insert(tk.END, "Just a text Widget\nin two lines\n")'''

#parameters for file browsing when uploading a vid
options={}
options['defaultextension'] = '.mp4'
options['filetypes'] = [('all files', '.*'), ('mp4 files', '.mp4')]
options['initialdir'] = 'C:\\'
options['initialfile'] = 'myfile.mp4'
options['parent'] = root
options['title'] = 'Choose a file'

upload_name = None
upload_btn = None
the_sender = None
status = 0
cancel = None
back = None
in_upload_screen = False

rows = []
cols = []
tasks.print_main = True

while True:
    if tasks.print_main:
        tasks.print_main = False
        canvas = tk.Canvas(embed, width=528, height=200)
        canvas.pack(side="top", fill="both", expand=True)
        helv36 = Font(family="Times", weight="bold", slant="italic", size=87)
        canvas_id = canvas.create_text(50, 30, anchor="nw", font=(helv36), fill='green')

        canvas.itemconfig(canvas_id, text="EyeTube")

        canvas2 = tk.Canvas(embed, width=528, height=200)
        canvas2.pack(side="top", fill="both", expand=True)

        #tk.Label(text='search').pack(side=tk.TOP,padx=10,pady=10)
        entry = tk.Entry(canvas2, width=30)
        entry.pack(side=tk.TOP, padx=10, pady=10)
        tk.Button(canvas2, text='search', command=onsearch).pack(side=tk.TOP)

        canvas3 = tk.Canvas(embed, width=528, height=200)
        canvas3.pack(side="top", fill="both", expand=True)

        canvas4 = tk.Canvas(embed, width=528, height=100)
        canvas4.pack(side="bottom", fill="both", expand=True)

        text = tk.Button(canvas4, text='upload a vid ;)', width=20, command=tasks.upload_screen)
        text.pack(side='top')

        canvas.configure(background=SCREEN_COLOR)
        canvas2.configure(background=SCREEN_COLOR)
        canvas3.configure(background=SCREEN_COLOR)
        canvas4.configure(background=SCREEN_COLOR)

    if com.print_results:

        for row in rows:
            for col in row:
                col.destroy()
        canvas3.delete("all")

        rows = []
        cols = []

        for i in com.res_list:
            if len(i) < 3:
                com.res_list.remove(i)

        if len(com.res_list) > 1:
            for row, lst in enumerate(com.res_list):
                cols = []
                if row > 0:
                    b = tk.Button(canvas3, text=lst[0], bg='cyan', command=lambda x=0, y=row: onclick(x, y))
                    b.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
                    cols.append(b)
                else:
                    label = tk.Label(canvas3, text=lst[0], borderwidth=0, width=10)
                    label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
                    cols.append(label)

                label = tk.Label(canvas3, text=lst[1], borderwidth=0, width=10)
                label.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
                cols.append(label)

                label = tk.Label(canvas3, text=lst[2], borderwidth=0, width=10)
                label.grid(row=row, column=2, sticky="nsew", padx=1, pady=1)
                cols.append(label)

                rows.append(cols)


            canvas3.grid_columnconfigure(0, minsize=228)
            canvas3.grid_columnconfigure(1, minsize=150)
            canvas3.grid_columnconfigure(2, minsize=150)
            #root.grid_rowconfigure(0, weight=1)
            #root.grid_columnconfigure(0, weight=1)
        else:
            label = tk.Label(canvas3, text='no related video names was found', borderwidth=0, width=10)
            label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
            canvas3.grid_columnconfigure(0, minsize=528)

        com.print_results = False
        print '&&&', com.res_list



    elif not tasks.mov_name == '':
        movie_name = tasks.mov_name
        tasks.mov_name = ''
        print movie_name

        canvas2.destroy()
        canvas.destroy()
        canvas3.destroy()
        canvas4.destroy()
        root.update()

        #canvas = tk.Canvas(embed, width=528, height=1)
        #canvas.pack(side="bottom", fill="both", expand=True)

        text = tk.Button(embed, text="BACK", command=tasks.close)
        #img = tk.PhotoImage(file="backbutton.gif") # make sure to add "/" not "\"
        #text.config(image=img)
        text.pack(side='bottom')
        root.update()
        #text.destroy()

        sock.send('parts:' + movie_name)
        data = sock.recv(1024)
        com.handle_message(data)
        numpart = com.partnum

        the_saver = None

        if not cach.in_cashe(movie_name, numpart) and not numpart == -1:
            sock.send('Watch:' + movie_name + ':!:' + '0')
            data = sock.recv(1024)
            com.handle_message(data)
            the_saver = com.receive
            #print 'you are not supposed to be in here'

        if numpart != -1:

            #gets all files in cache
            incashe = [f for f in listdir(CASHE + movie_name + '\\') if isfile(join(CASHE + movie_name + '\\', f))]
            t = time.time()

            #checks if enough parts went in
            while not isfile(CASHE + movie_name + '\\' + "000.mpg") or len(incashe) < 5:
                incashe = [f for f in listdir(CASHE + movie_name + '\\') if isfile(join(CASHE + movie_name + '\\', f))]
                #timeout for waiting is 15 minutes
                root.update()
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
                #vid_bar.show_video_bar(numpart, num, numpart)
                update_bar_by_params(the_saver, num, numpart)

                img = pygame.image.load("pause.png")
                movie_screen.blit(img, (444, 380))
                play_rect = img.get_rect()
                play_rect.move_ip(444, 380)


                playing = True
                pause = False
                #starts the audio
                player.start()
                #starts movie
                movie.play()

                num += 1

                while playing:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or tasks.kill:
                            movie.stop()
                            #will stop the audio too
                            playing = False
                            tasks.print_main = True
                            text.destroy()
                            if the_saver and the_saver.isAlive():
                                the_saver.running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if vid_bar.bar.collidepoint(pos) and not pause:

                                movie.stop()
                                playing = False
                                while player.isAlive():
                                    pass

                                playing = True

                                num = int((float(pos[0])/(vid_bar.bar_length-2)) * numpart)
                                print num

                                if not isfile(CASHE + movie_name + '\\' + get_part_video_num(num) + '.mpg') or not isfile(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav') or not isfile(CASHE + movie_name + '\\' + get_part_video_num(num+1) + '.wav'):
                                    if the_saver and the_saver.isAlive():
                                        sock.send('from:' + str(the_saver.port) + ':' + str(num))
                                        t = time.time()
                                    else:
                                        sock.send('Watch:' + movie_name + ':!:' + str(num))
                                        data = sock.recv(1024)
                                        com.handle_message(data)
                                        the_saver = com.receive

                                while not isfile(CASHE + movie_name + '\\' + get_part_video_num(num) + '.mpg') or not isfile(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav') or not isfile(CASHE + movie_name + '\\' + get_part_video_num(num+1) + '.wav'):
                                    pygame.event.pump()
                                    if isinstance(the_saver.part, basestring):
                                        update_bar_by_params(the_saver, num, numpart)
                                    screen.blit(movie_screen, (0, 0))
                                    pygame.display.update()
                                    #if time.time() - t > 3:
                                    #    sock.send('from:' + str(the_saver.port) + ':' + str(num))

                                wf = wave.open(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav', 'rb')
                                while True:
                                    try:
                                        wf2 = wave.open(CASHE + movie_name + '\\' + get_part_video_num(num + 1) + '.wav', 'rb')
                                        break
                                    except:
                                        pass
                                #audio player
                                player = Music_player(num)
                                player.start()
                                movie = pygame.movie.Movie(CASHE + movie_name + '\\' + get_part_video_num(num) + '.mpg')
                                movie.set_display(movie_screen, [0, 0, 528, 360])
                                movie.play()
                                num += 1

                                update_bar_by_params(the_saver, num, numpart)

                            elif play_rect.collidepoint(pos):
                                if pause:
                                    pygame.draw.rect(movie_screen, (255, 255, 255), play_rect)
                                    img = pygame.image.load("pause.png")
                                    movie_screen.blit(img, (444, 380))
                                    player.pause = False
                                    movie.pause()
                                    pause = False
                                else:
                                    pygame.draw.rect(movie_screen, (255, 255, 255), play_rect)
                                    img = pygame.image.load("play.png")
                                    movie_screen.blit(img, (444, 380))
                                    movie.pause()
                                    player.pause = True
                                    pause = True



                    if not movie.get_busy() and playing and not pause and isfile(CASHE + movie_name + '\\' + get_part_video_num(num) + '.mpg') and isfile(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav'):
                        print num
                        #next video part
                        movie = pygame.movie.Movie(CASHE + movie_name + '\\' + get_part_video_num(num) + '.mpg')
                        movie.set_display(movie_screen, [0, 0, 528, 360])
                        movie.play()
                        num += 1

                        update_bar_by_params(the_saver, num, numpart)

                    if not player.next and playing and not pause and isfile(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav'):
                        if player.streamnum == 2:
                            wf = wave.open(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav', 'rb')
                        else:
                            wf2 = wave.open(CASHE + movie_name + '\\' + get_part_video_num(num) + '.wav', 'rb')
                        player.next = True

                    if tasks.kill:
                        movie.stop()
                        playing = False
                        tasks.print_main = True
                        text.destroy()
                        tasks.kill = False
                        if the_saver and the_saver.isAlive():
                            the_saver.running = False

                    update_bar_by_params(the_saver, num, numpart)
                    screen.blit(movie_screen, (0, 0))
                    pygame.display.update()
                    clock.tick(FPS)

                    root.update()

                pygame.quit()
                #sys.exit()

    elif tasks.print_upload:
        tasks.print_upload = False

        in_upload_screen = True

        canvas2.destroy()
        #canvas.destroy()
        canvas3.destroy()
        canvas4.destroy()

        canvas2 = tk.Canvas(embed, width=528, height=300)
        canvas2.pack(side="top", fill="both", expand=True)
        canvas2.configure(background=SCREEN_COLOR)

        choose = tk.Button(canvas2, text='CHOOSE A VIDEO TO UPLOAD', command=choosefile)
        choose.pack(side='top')

        back = tk.Button(canvas2, text='BACK', command=tasks.out_of_upload)
        back.pack(side='bottom')


    elif not tasks.upload_chosen == '' and in_upload_screen:
        upload_path = tasks.upload_chosen
        tasks.upload_chosen = ''
        print upload_path, '!@#$%^&*()_+'

        if not upload_name:
            upload_name = tk.Label(canvas2)

        if upload_path[-4:] == '.mp4':

            vid = video_manager.Video_manager(upload_path)

            if vid.get_size() < 500 and vid.get_length() < 3600 and not upload_btn:

                entry = tk.Entry(canvas2, width=30)
                entry.pack(side=tk.TOP, padx=10, pady=10)

                upload_btn = tk.Button(canvas2, text='UPLOAD VID', command=on_upload)
                upload_btn.pack(side='top')

                upload_name.config(font=("Courier", 16),background=SCREEN_COLOR,foreground="black",text='CHOOSE A NAME')
                upload_name.pack(side=tk.TOP,padx=10,pady=10)

            elif vid.get_size() >= 500:

                upload_name.config(font=("Courier", 10),background=SCREEN_COLOR,foreground="red",text='the video needs to be less than 500 MB')
                upload_name.pack(side=tk.TOP,padx=10,pady=10)

            elif vid.get_length() >= 3600:

                upload_name.config(font=("Courier", 10),background=SCREEN_COLOR,foreground="red",text='the video needs to be less than a hour long')
                upload_name.pack(side=tk.TOP,padx=10,pady=10)

        else:

            upload_name.config(font=("Courier", 16),background=SCREEN_COLOR, foreground="red",text='you need an mp4 file')
            upload_name.pack(side=tk.TOP,padx=10,pady=10)

    elif com.upload_num > 0 and in_upload_screen:

        #in this case the upload started
        if com.upload_num == 1:

            upload_name.config(font=("Courier", 16),background=SCREEN_COLOR,foreground="black",text='UPLOADING: ' + upload_path)
            upload_name.pack(side=tk.TOP,padx=10,pady=10)

            progress = ttk.Progressbar(canvas2, orient="horizontal", length=450, mode="determinate")

            progress["value"] = 0
            maxbytes = vid.get_size(0)
            progress["maximum"] = maxbytes

            progress.pack(side='top')

            status = 0
            the_sender = com.uploader

            cancel = tk.Button(canvas2, text='CANCEL UPLOAD', command=on_cancel)
            cancel.pack(side='bottom')

        #in this case the upload request sent but the server denied it because of the file
        elif com.upload_num == 2 and in_upload_screen:

            upload_name.config(font=("Courier", 16),background=SCREEN_COLOR,foreground="red",text='file was already uploaded')
            upload_name.pack(side=tk.TOP,padx=10,pady=10)

        #in this case the upload request sent but the server denied it because of the name
        elif com.upload_num == 3:

            upload_name.config(font=("Courier", 16),background=SCREEN_COLOR,foreground="red",text='name already exists')
            upload_name.pack(side=tk.TOP,padx=10,pady=10)

        elif com.upload_num == 7:

            upload_name.config(font=("Courier", 16),background=SCREEN_COLOR,foreground="red",text='you need to choose a name!')
            upload_name.pack(side=tk.TOP,padx=10,pady=10)


        com.upload_num = 0


    if the_sender and not status == the_sender.progress and in_upload_screen:

        #updates the upload bar
        status = the_sender.progress
        progress["value"] = status

        #in this case the upload ended and the video is being processed
        if status >= maxbytes:

            upload_name.config(font=("Courier", 10),background=SCREEN_COLOR,foreground="black",text='processing video... this may take a few minutes')
            upload_name.pack(side=tk.TOP,padx=10,pady=10)

            cancel.destroy()


    if tasks.upload_canceled and in_upload_screen:

        tasks.upload_canceled = False

        if the_sender:
            the_sender = None

        if cancel:
            cancel.destroy()

        if progress:
            progress.destroy()
            status = 0

        upload_name.config(font=("Courier", 16),background=SCREEN_COLOR,foreground="black",text='UPLOAD CANCELED')
        upload_name.pack(side=tk.TOP,padx=10,pady=10)


    if the_sender and tasks.upload_complete and in_upload_screen:

        upload_name.config(font=("Courier", 16),background=SCREEN_COLOR,foreground="black",text='UPLOAD COMPLETE')
        upload_name.pack(side=tk.TOP,padx=10,pady=10)
        the_sender = None
        
        
    if tasks.back_from_upload and in_upload_screen:

        if cancel.winfo_exists() == 1:
            answer = tkMessageBox.askyesno("eyetube manager", "by getting back you are canceling the uploading are you sure you want to cancel uploading?")
            if the_sender:
                the_sender.sending = False
        in_upload_screen = False
        tasks.back_from_upload = False
        the_sender = None
        upload_btn = None
        cancel = None
        upload_name = None
        canvas2.destroy()
        canvas.destroy()
        tasks.main_screen()



    root.update()



sock.close()

