# -*- coding: utf-8 -*-

'''import numpy as np
import cv2

# Capture video from file
cap = cv2.VideoCapture("D:\\dogs.mp4")

while True:

    ret, frame = cap.read()

    if ret == True:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame',gray)


        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()'''


import pygame
import time
import sys
import os

FPS = 30

pygame.init()
clock = pygame.time.Clock()
movie = pygame.movie.Movie('D:\\here\\00.mpg')
screen = pygame.display.set_mode(movie.get_size())
movie_screen = pygame.Surface(movie.get_size()).convert()

movie_len = movie.get_length()

movie.set_display(movie_screen)
movie.play()

num = '01'
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            movie.stop()
            playing = False

    if movie.get_time() >= movie_len:
        print num
        movie = pygame.movie.Movie('D:\\here\\' + num + '.mpg')
        movie.set_display(movie_screen)
        movie.play()

        num = str(int(num) + 1)
        if len(num) == 1:
            num = '0' + num
        while not os.path.exists('D:\\here\\' + num + '.mpg') and int(num) < 30:
            num = str(int(num) + 1)
            if len(num) == 1:
                num = '0' + num
        if num == '30':
            movie.stop()
            playing = False


    screen.blit(movie_screen, (0, 0))
    pygame.display.update()
    clock.tick(FPS)


pygame.quit()