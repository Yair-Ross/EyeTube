# -*- coding: utf-8 -*-
import pygame
import time
import sys


def get_part_video_num(num):
    if len(str(num)) == 1:
        return '00' + str(num)
    elif len(str(num)) == 2:
        return '0' + str(num)
    else:
        return str(num)


"""
FPS = 30

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
'''t = time.time()
while time.time() - t < 0.1:
    pass
movie.stop()
time.sleep(30)'''

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

pygame.quit()"""



'''FPS = 30

pygame.init()
clock = pygame.time.Clock()
movie = pygame.movie.Movie("D:\\hobbit.mpg")
screen = pygame.display.set_mode(movie.get_size())
movie_screen = pygame.display.set_mode((1920, 1080))
pygame.display.flip()

movie.set_display(movie_screen, [0, 0, 1920, 1080])
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

pygame.quit()'''


'''import pygame
pygame.init()
pygame.display.set_mode((200,100))
pygame.mixer.music.load("D:\\soundhobhob.mp3")
pygame.mixer.music.play(0)

clock = pygame.time.Clock()
clock.tick(10)
while pygame.mixer.music.get_busy():
    pygame.event.poll()
    clock.tick(10)'''


import pygame

pygame.init()
FPS = 60


clock = pygame.time.Clock()
pygame.mixer.quit()
movie = pygame.movie.Movie("D:\\ssss.mpg")
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

pygame.quit()


