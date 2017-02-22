# -*- coding: utf-8 -*-
#import pygame


def main():
    """
    Add Documentation here
    """


    '''
    subprocess.call('ffmpeg -r 10 -i frame%03d.png -r ntsc '+str('D:\dawg.mpg'), shell=True)
    #subprocess.call('ffmpeg -i D:\dogs.mp4 -vcodec mpeg1video -acodec libmp3lame -intra D:\dawg.mpg', shell=True)
    #subprocess.call(['ffmpeg', '-i', 'D:\dogs.mp4', '-vcodec', 'mpeg1video', '-acodec', 'libmp3lame', '-intra', 'D:\dawg.mpg'])'''

    '''import subprocess
    cmd = ['ffmpeg', '-i', 'D:\dogs.mp4', '-vcodec', 'mpeg1video', '-acodec', 'libmp3lame', '-intra', 'D:\dawg.mpg']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              stdin=subprocess.PIPE)
    out, err = p.communicate('foo\nfoofoo\n')
    print out'''

    '''command = 'ffmpeg -i D:\dogs.mp4 -vcodec mpeg1video -acodec libmp3lame -intra D:\dawg.mpg'
    p = subprocess.Popen(command, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]'''

    '''from subprocess import Popen
    p = Popen(["what.bat"])'''

    #import subprocess
    #p = subprocess.call('ffmpeg -i D:\dogs.mp4 -vcodec mpeg1video -acodec libmp3lame -intra D:\dawg.mpg', shell=True)


    '''def increase(time):
        if time[6:] != '55':
            time = time[:6] + str(int(time[6:])+5)
            if len(time) == 7:
                time = time[:6] + '05'
        return time'''



    '''class Time():

        def __init__(self):
            self.seconds = 0
            self.minutes = 0
            self.hours = 0

        def increase_num(self, num_to_increase):
            pass

        def return_time(self):
            return str(self.seconds) + ':' + str(self.minutes) + ':' + str(self.hours)'''


    '''import subprocess
    import sys
    #command = 'ffmpeg -i E:\\tmp\\cc.mpg -vcodec copy -acodec copy -ss 00:00:00 -t 00:00:25 E:\\tmp\\test_subj\\vanvan.mpg'
    command = 'ls'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print
    print
    print
    print
    print 'abxd'
    print
    print
    print
    print
    output = sys.stdin.read(0)
    print output
    print process.returncode'''


    '''import subprocess
    command = 'ffmpeg -i E:\\tmp\\cc.mpg -vcodec copy -acodec copy -ss 00:00:00 -t 00:00:30 E:\\tmp\\test_subj\\a1.mpg \   -vcodec copy -acodec copy -ss 00:00:30 -t 00:01:00 E:\\tmp\\test_subj\\a1.mpg'
    p = subprocess.call(command)'''


    '''import datetime
    import subprocess
    import time
    #t1 = '00:00:00'
    #t2 = '00:00:05'
    #d = [('00:00:00', '00:00:05'), ('00:00:06', '00:00:10'), ('00:00:11', '00:00:15'), ('00:00:16', '00:00:20'), ('00:00:21', '00:00:25')]

    t = datetime.time(0, 0, 0)
    t2 = datetime.time(0, 0, 5)

    for i in range(10):

        p = subprocess.call('ffmpeg -i E:\\tmp\\cc.mpg -vcodec copy -acodec copy -ss %s -t %s E:\\tmp\\test_subj\\weird%s.mpg' % (str(t), str(t2), i))
        #print 'ffmpeg -i D:\dawg.mpg -vcodec copy -acodec copy -ss %s -t %s D:\ddog%s.mpg' % (t1, t2, i)
        #p = subprocess.call('ffmpeg -i D:\dd.mpg -vcodec copy -acodec copy -ss %s -t %s D:\a%s.mpg' % (t1, t2, i))
        #print t1
        #t1 = increase(t1)
        #print
        #print t2
        #t2 = increase(t1)
        #print
        #print
        #print d[i][0], '   ', d[i][1]
        t = datetime.timedelta(seconds=i*5)
        t2 = datetime.timedelta(seconds=i*5 + 5)

        print t
        print
        print t2
        print
        print
        time.sleep(3)'''





    '''import pygame
    import time
    import sys

    FPS = 30

    pygame.init()
    clock = pygame.time.Clock()
    movie = pygame.movie.Movie("E:\\tmp\\test_subj\\out000.mpg")
    screen = pygame.display.set_mode(movie.get_size())
    movie_screen = pygame.Surface(movie.get_size()).convert()

    movie_len = movie.get_length()

    movie.set_display(movie_screen)
    movie.play()

    num = 1
    playing = True
    temp = movie_len
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                playing = False

        if movie.get_time() >= movie_len:
            print num
            movie = pygame.movie.Movie('E:\\tmp\\test_subj\\out00' + str(num) + '.mpg')
            movie_len = movie.get_length() - temp
            temp = movie.get_length()
            movie.set_display(movie_screen)
            movie.play()
            num += 1

        screen.blit(movie_screen, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


    pygame.quit()'''


    '''def get_part_video_num(num):
        if len(str(num)) == 1:
            return '00' + str(num)
        elif len(str(num)) == 2:
            return '0' + str(num)
        else:
            return str(num)


    import pygame
    import time
    import sys

    FPS = 30

    pygame.init()
    clock = pygame.time.Clock()
    pygame.mixer.quit()
    movie = pygame.movie.Movie("D:\\hell_yeh\\000.mpg")
    screen = pygame.display.set_mode(movie.get_size())
    movie_screen = pygame.Surface(movie.get_size()).convert()

    movie.set_display(movie_screen)
    movie.set_volume(0.5)
    movie.play()

    num = 1
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                playing = False

        if not movie.get_busy():
            print num
            movie = pygame.movie.Movie("D:\\hell_yeh\\" + get_part_video_num(num) + '.mpg')
            movie.set_display(movie_screen)
            movie.set_volume(0.5)
            movie.play()
            num += 1

        screen.blit(movie_screen, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


    pygame.quit()'''



    '''def get_part_video_num(num):
        if len(str(num)) == 1:
            return '00' + str(num)
        elif len(str(num)) == 2:
            return '0' + str(num)
        else:
            return str(num)


    import pygame


    FPS = 30

    pygame.init()
    pygame.mixer.quit()
    clock = pygame.time.Clock()
    movie = pygame.movie.Movie("D:\\hell_yeh\\output000.mpg")
    screen = pygame.display.set_mode(movie.get_size())
    movie_screen = pygame.Surface(movie.get_size()).convert()

    movie.set_display(movie_screen)
    movie.set_volume(0.5)
    movie.play()

    num = 1
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                playing = False

        if not movie.get_busy():
            print num
            movie = pygame.movie.Movie("D:\\hell_yeh\\output" + get_part_video_num(num) + '.mpg')
            movie = pygame.movie.Movie("D:\\hell_yeh\\output" + get_part_video_num(num) + '.mpg')
            movie.set_display(movie_screen)
            movie.set_volume(0.5)
            movie.play()
            num += 1

        screen.blit(movie_screen, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


    pygame.quit()'''

    def get_part_video_num(num):
        if len(str(num)) == 1:
            return '00' + str(num)
        elif len(str(num)) == 2:
            return '0' + str(num)
        else:
            return str(num)

    COPY_PATH = "D:\\mpsplits\\"
    PASTE_PATH = "D:\\mas\\"
    n = 0

    import subprocess
    #for i in range(20):
    #    p = subprocess.call('ffmpeg -i %s.mp4 %s.wav' % (COPY_PATH+get_part_video_num(n), PASTE_PATH+get_part_video_num(n)))
    #    n += 1

    n = 0
    for i in range(20):
        p = subprocess.call('ffmpeg -i %s.mp4 -target ntsc-vcd -vcodec mpeg1video -an %s.mpg' % (COPY_PATH+get_part_video_num(n), PASTE_PATH+get_part_video_num(n)))
        n += 1
    print 'nehenaknu im gui'
    pass




    '''
    f = open('D:\\orion_1.mpg', 'rb')
    g = open('D:\\grb_1.mpg', 'rb')
    num = 0
    a = f.read(2)
    b = g.read(2)
    print a
    print b
    while a == b:
        a = f.read(1)
        b = g.read(1)
        num += 1
    print num + 1
    f.close()
    g.close()
    '''



    '''
    f = open('D:\\orion_1.mpg', 'rb')
    s = f.read(23)
    f.seek(0)

    n = 'a'
    j = 0
    while n != '':
        n = f.read(200000)
        g = open('D:\\victory' + str(j) + '.mpg', 'wb')
        g.write(s + n)
        g.close()
        j += 1

    f.close()'''


    """f = open('D:\\orion_1.mpg', 'rb')
    a = f.read(1000000)
    f.close()
    g = open('D:\\t1.mpg', 'wb')
    g.write(a)
    g.close()"""

    '''
    f = open('D:\\orion_1.mpg', 'rb')
    a = f.read(1000000)
    b = f.read()
    f.close()

    g = open('D:\\t2.mpg', 'wb')
    g.write(a)
    g.close()

    n = open('D:\\t3.mpg', 'wb')
    n.write(b)
    n.close()'''

    '''FPS = 60

    pygame.init()
    clock = pygame.time.Clock()
    movie = pygame.movie.Movie('F:\\grb_1.MPG')
    screen = pygame.display.set_mode(movie.get_size())
    movie_screen = pygame.Surface(movie.get_size()).convert()

    movie.set_display(movie_screen)
    movie.play()


    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                playing = False

        screen.blit(movie_screen,(0,0))
        pygame.display.update()
        clock.tick(FPS)

    print 'a'
    movie = pygame.movie.Movie('F:\\grb_2.MPG')

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                playing = False

        screen.blit(movie_screen,(0,0))
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()'''


    '''def play_movie(path):
        from os import startfile
        startfile(path)

    class Video(object):
        def __init__(self,path):
            self.path = path

        def play(self):
            from os import startfile
            startfile(self.path)

    class Movie_MP4(Video):
        type = "MP4"

    movie = Movie_MP4(r"F:\dogs.mp4")
    if raw_input("Press enter to play, anything else to exit") == '':
        movie.play()'''
    '''
    f = open('D:\\orion_1.mpg', 'rb')
    s = f.read(23)
    s = ":".join("{:02x}".format(ord(c)) for c in s)
    print s
    f.close()'''


if __name__ == '__main__':
    main()