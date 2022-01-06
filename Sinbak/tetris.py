import sys
import random
import pygame
from pygame.locals import *

# from drawgird import CELL_SIZE

#pygame에사 사용할 전역 변수 : 1. size 2. screen 3. clock
pygame.init() #pygame 초기화
BLACK = (0,0,0)
WHITE = (255,255,255)
pygame.key.set_repeat(30, 30)
pygame.display.set_caption('Tetris') 
clock = pygame.time.Clock() #clock 프레임
col= 12
row = 22
cell_size = 18
Screen_Width = cell_size*(col+6)
Screen_Height = cell_size*row
size = [Screen_Width, Screen_Height]
screen = pygame.display.set_mode(size) #size


while True:
    screen.fill(BLACK)
            #키 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    for col_index in range(col):
        for row_index in range(row):
            pygame.draw.rect(screen,WHITE, pygame.Rect(col_index*cell_size, row_index*cell_size, cell_size,cell_size),1)
    pygame.display.update()
    clock.tick(30)
