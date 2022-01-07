import sys
import pygame
from pygame.locals import *
from math import sqrt
from random import randint

clock = pygame.time.Clock()
screen = pygame.display.set_mode([600, 600])

Width = 14
Height = 21
Field = []
Psize = 24
Pgsize = Psize + 1

COLORS = ((0, 0, 0), (255, 165, 0), (0, 0, 255), (0, 255, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 0, 0), (128, 128, 128))
BLOCK = None
NBlock = None
BLOCK_DATA = (
    (
        ( ## ㅣ모양
            0, 1, 0, 0,
            0, 1, 0, 0,
            0, 1, 0, 0,
            0, 1, 0, 0
        ), ( 
            0, 0, 0, 0,
            1, 1, 1, 1,
            0, 0, 0, 0,
            0, 0, 0, 0
        ), (
            0, 0, 1, 0,
            0, 0, 1, 0,
            0, 0, 1, 0,
            0, 0, 1, 0
        ), (
            0, 0, 0, 0,
            0, 0, 0, 0,
            1, 1, 1, 1,
            0, 0, 0, 0)
    ), (
        ( ## ㄱ모양
            0, 0, 2, 
            2, 2, 2,
            0, 0, 0
        ), (
            0, 2, 0, 
            0, 2, 0,
            0, 2, 2
        ), (
            0, 0, 0,
            2, 2, 2,
            2, 0, 0
        ), (
            2, 2, 0,
            0, 2, 0,
            0, 2, 0)
    ), (
        ( ## ㅗ모양
            0, 3, 0,
            3, 3, 0,
            0, 3, 0
        ), (
            0, 3, 0,
            3, 3, 3,
            0, 0, 0
        ), (
            0, 3, 0,
            0, 3, 3,
            0, 3, 0
        ), (
            0, 0, 0,
            3, 3, 3,
            0, 3, 0)
    ), ( ## ㅁ모양
        (4, 4, 4, 4),
        (4, 4, 4, 4),
        (4, 4, 4, 4),
        (4, 4, 4, 4)
    ), ( ## ㄴ모양
        ( 
            5, 0, 0,
            5, 5, 5,
            0, 0, 0
        ), (
            0, 5, 5,
            0, 5, 0,
            0, 5, 0
        ), (
            0, 0, 0,
            5, 5, 5,
            0, 0, 5
        ), (
            0, 5, 0,
            0, 5, 0,
            5, 5, 0)
    ), ( ## 역Z모양
        (
            0, 6, 6,
            6, 6, 0,
            0, 0, 0
        ), (
            0, 6, 0,
            0, 6, 6,
            0, 0, 6
        ), (
            0, 0, 0,
            0, 6, 6,
            6, 6, 0
        ), (
            6, 0, 0,
            6, 6, 0,
            0, 6, 0)
    ) , (
        ( ## Z모양
            7, 7, 0,
            0, 7, 7,
            0, 0, 0
        ),(
            0, 7, 0,
            7, 7, 0,
            7, 0, 0
        ), (
            0, 0 ,0,
            7, 7, 0,
            0, 7, 7
        ), (
            0, 0, 7,
            0, 7, 7,
            0, 7, 0
        )
    )
)

class Setting(object):
    def Init(self):   
        pygame.init()
        pygame.display.set_caption("Tetris")
        done = False
        
    def Playing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def Set_Field(self):
        for i in range(Height - 1):
            Field.insert(0, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        Field.insert(Height - 1, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    def Draw_Field(self):
        for i in range(Height):
            for j in range(Width):
                val = Field[i][j]
                color = COLORS[val]
                pygame.draw.rect(screen, color,(Pgsize + j * Pgsize, Pgsize + i * Pgsize, Psize, Psize))

    def Start(self):
        while True:
            clock.tick(10)
            self.Set_Field()
            self.Draw_Field()
            self.Playing()
            pygame.display.flip()

class Block:
    def Block_init(self):
        self.size = int(sqrt(len(self.data)))
        self.turn = 0
        self.type = BLOCK_DATA[0]
        self.data = self.type[self.turn]
        self.x = randint(2, 8 - self.size)
        self.y = 1 - self.size

    def Draw_Block(self):
        for y in range(self.size):
            for x in range(self.size):
                index = y * self.size + x
                val = self.data[index]
                if 0 <= y + self.y < Height and 0 <= x + self.x < Width and val != 0:
                    f_x = Pgsize + (x + self.x) * Pgsize
                    f_y = Pgsize + (y + self.y) * Pgsize
                    pygame.draw.rect(screen, COLORS[val], (f_x, f_y, Psize, Psize))


if __name__ == "__main__":
    game = Setting()
    game.Start()



