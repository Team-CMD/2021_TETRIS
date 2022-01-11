import sys, pygame
from math import sqrt
from random import randint

pygame.init()
screen = pygame.display.set_mode([600, 600])
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()
WIDTH = 12
HEIGHT = 22
INTERVAL = 40
FIELD = []
COLORS = ((0, 0, 0), (255, 165, 0), (0, 0, 255), (0, 255, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 0, 0), (128, 128, 128))
BLOCK = None
NEXT_BLOCK = None
PSIZE = 24 
PGSIZE = PSIZE + 1 
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
def Set_Field():
    for i in range(HEIGHT - 1):
        FIELD.insert(0, [-1, 0,0,0,0,0,0,0,0,0,0 ,-1])    
    FIELD.insert(HEIGHT - 1, [-1, -1,-1,-1,-1,-1,-1,-1,-1,-1,-1 ,-1])

def Draw_Field():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            val = FIELD[y][x]
            color = COLORS[val]
            pygame.draw.rect(screen, color, (PGSIZE + x * PGSIZE, PGSIZE + y * PGSIZE, PSIZE, PSIZE ))

class Block:
    def __init__(self, count):
        self.turn = randint(0, 3) 
        self.type = BLOCK_DATA[randint(0, 6)]  
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data)))
        self.xpos = randint(2, 8 - self.size)
        self.ypos = 1 - self.size
        self.fire = count + INTERVAL

    def update(self, count):
        erased = 0
        if is_overlapped(self.xpos, self.ypos + 1, self.turn):
            for y in range(BLOCK.size):
                for x in range(BLOCK.size):
                    index = y * self.size + x
                    val = BLOCK.data[index]
                    if 0 <= self.ypos + y < HEIGHT and 0 <= self.xpos + x < WIDTH and val != 0:
                            FIELD[self.ypos + y][self.xpos + x] = val

        if self.fire < count:
            self.fire = count + INTERVAL
            self.ypos += 1
        return erased

    def draw(self):
        for y in range(self.size):
            for x in range(self.size):
                index = y * self.size + x
                val = self.data[index]
                if 0 <= y + self.ypos < HEIGHT and 0 <= x + self.xpos < WIDTH and val != 0:
                    f_xpos = PGSIZE + (x + self.xpos) * PGSIZE
                    f_ypos = PGSIZE + (y + self.ypos) * PGSIZE
                    pygame.draw.rect(screen, COLORS[val], (f_xpos, f_ypos, PSIZE, PSIZE))  

def Next_block(count):
    global BLOCK, NEXT_BLOCK
    BLOCK = NEXT_BLOCK if NEXT_BLOCK != None else Block(count)
    NEXT_BLOCK = Block(count)

def is_overlapped(xpos, ypos, turn):
    return False

def main():
    global INTERVAL
    count = 0
    
    Next_block(INTERVAL)
    Set_Field()

    while True:
        clock.tick(50)
        count += 5
        if count % 1000 == 0:
            INTERVAL = max(1, INTERVAL - 2)
        erased = BLOCK.update(count)

        Draw_Field()
        BLOCK.draw()
        pygame.display.update()
    
main()
pygame.quit()
