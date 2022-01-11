import pygame as pg
import sys
from random import randint
from math import sqrt

pg.init()
smallfont = pg.font.SysFont(None,36)
largefont = pg.font.SysFont(None,72)
pg.key.set_repeat(30,30)
pg.display.set_caption("Tetris")
CLOCK = pg.time.Clock()

PIECE_SIZE = 24
PIECE_GRID_SIZE = PIECE_SIZE + 1
BOARD_WIDTH = 14
BOARD_HEIGHT = 21
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
INTERVAL = 40
COLORS = ((0, 0, 0), (255, 165, 0), (0, 0, 255), (0, 255, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 0, 0), (128, 128, 128))
BOARD = []
SCREEN = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
BLOCK = None
NEXT_BLOCK = None
BLOCK_DATA = (
    (
        (0, 0, 1, \
         1, 1, 1, \
         0, 0, 0),
        (0, 1, 0, \
         0, 1, 0, \
         0, 1, 1),
        (0, 0, 0, \
         1, 1, 1, \
         1, 0, 0),
        (1, 1, 0, \
         0, 1, 0, \
         0, 1, 0),
    ), (
        (2, 0, 0, \
         2, 2, 2, \
         0, 0, 0),
        (0, 2, 2, \
         0, 2, 0, \
         0, 2, 0),
        (0, 0, 0, \
         2, 2, 2, \
         0, 0, 2),
        (0, 2, 0, \
         0, 2, 0, \
         2, 2, 0)
    ), (
        (0, 3, 0, \
         3, 3, 3, \
         0, 0, 0),
        (0, 3, 0, \
         0, 3, 3, \
         0, 3, 0),
        (0, 0, 0, \
         3, 3, 3, \
         0, 3, 0),
        (0, 3, 0, \
         3, 3, 0, \
         0, 3, 0)
    ), (
        (4, 4, 0, \
         0, 4, 4, \
         0, 0, 0),
        (0, 0, 4, \
         0, 4, 4, \
         0, 4, 0),
        (0, 0, 0, \
         4, 4, 0, \
         0, 4, 4),
        (0, 4, 0, \
         4, 4, 0, \
         4, 0, 0)
    ), (
        (0, 5, 5, \
         5, 5, 0, \
         0, 0, 0),
        (0, 5, 0, \
         0, 5, 5, \
         0, 0, 5),
        (0, 0, 0, \
         0, 5, 5, \
         5, 5, 0),
        (5, 0, 0, \
         5, 5, 0, \
         0, 5, 0)
    ), (
        (6, 6, \
        6, 6),
        (6, 6, \
        6, 6),
        (6, 6, \
        6, 6),
        (6, 6, \
        6, 6)
    ), (
        (0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0),
        (0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0, \
         0, 0, 0, 0),
        (0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0),
        (0, 0, 0, 0, \
         0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0)
    )
)

class Block:
    def __init__(self, count):
        self.turn = randint(0,3)
        self.type = BLOCK_DATA[randint(0,6)]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data))) # 3 or 4
        self.xpos = randint(2,8-self.size)
        self.ypos = 1 - self.size
        self.fire = count + INTERVAL


    def update(self,count):
        erased = 0
        if is_Overlapped(self.xpos, self.ypos+1, self.turn):
            for y_offset in range(BLOCK.size):
                for x_offset in range(BLOCK.size):
                    index = y_offset * self.size + x_offset
                    val = BLOCK.data[index]
                    if 0 <= self.ypos+y_offset < BOARD_HEIGHT and \
                       0 <= self.xpos+x_offset < BOARD_WIDTH and val != 0:
                            BOARD[self.ypos+y_offset][self.xpos+x_offset] = val ## 값을 채우고, erase_line()을 통해 삭제되도록 한다.

            erased = erase_Line()
            go_Next_Block(count)

        if self.fire < count:
            self.fire = count + INTERVAL
            self.ypos += 1

        return erased

    def draw(self):
        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if 0 <= ypos + self.ypos < BOARD_HEIGHT and 0 <= xpos + self.xpos < BOARD_WIDTH and val != 0:
                x_pos = PIECE_GRID_SIZE + (xpos + self.xpos) * PIECE_GRID_SIZE
                y_pos = PIECE_GRID_SIZE + (ypos + self.ypos) * PIECE_GRID_SIZE
                pg.draw.rect(SCREEN,COLORS[val],(x_pos, y_pos,PIECE_GRID_SIZE,PIECE_GRID_SIZE))



def is_Game_Over():
    filled = 0
    for cell in BOARD[0]:
        if cell != 0:
            filled += 1
    return filled > 2 

def go_Next_Block(count):
    global BLOCK, NEXT_BLOCK
    BLOCK = NEXT_BLOCK if NEXT_BLOCK != None else Block(count)
    NEXT_BLOCK = Block(count)

def erase_Line():
        erased = 0
        ypos = BOARD_HEIGHT-2
        while ypos >= 0:
            if all(BOARD[ypos]):
                erased += 1
                del BOARD[ypos]
                BOARD.insert(0,[8, 0,0,0,0,0,0,0,0,0,0,0,0, 8])
            else:
                ypos -= 1
                
        return erased

def is_Overlapped(xpos, ypos, turn):
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            index = y_offset * BLOCK.size + x_offset
            val = data[index]

            if 0 <= xpos+x_offset < BOARD_WIDTH and \
                0 <= ypos+y_offset < BOARD_HEIGHT:
                if val != 0 and \
                    BOARD[ypos+y_offset][xpos+x_offset] != 0:
                    return True
    return False

def set_Game_Field():
    for i in range(BOARD_HEIGHT):
        row = []
        for j in range(BOARD_WIDTH):
            if i == BOARD_HEIGHT-1:
                row.append(8)
            else:
                if j == 0 or j == BOARD_WIDTH-1:
                    row.append(8)
                else:
                    row.append(0)
        BOARD.append(row)

def draw_Game_Field():
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            board = BOARD[i][j]
            color = COLORS[board]
            pg.draw.rect(SCREEN,color,(PIECE_GRID_SIZE + j*PIECE_GRID_SIZE, 
                        PIECE_GRID_SIZE + i*PIECE_GRID_SIZE , PIECE_SIZE , 
                        PIECE_SIZE ))

def draw_Current_Block():
    BLOCK.draw()

def draw_Next_Block():
    for y_offset in range(NEXT_BLOCK.size):
        for x_offset in range(NEXT_BLOCK.size):
            index = y_offset * NEXT_BLOCK.size + x_offset
            val = NEXT_BLOCK.data[index]
            #if 0 <= y_offset + self.ypos < HEIGHT and \
            #   0 <= x_offset + self.xpos < WIDTH and 
            if val != 0: ## 이 조건은 중요함! 0까지 그림을 그린다면, 쌓인 블록이 순간적으로 검정색이 됨.
                ## f_xpos = filed에서의 xpos를 계산함
                f_xpos = 460 + (x_offset) * PIECE_GRID_SIZE
                f_ypos = 100 + (y_offset) * PIECE_GRID_SIZE
                pg.draw.rect(SCREEN, COLORS[val],  
                (f_xpos, f_ypos, PIECE_SIZE, PIECE_SIZE))

def runGame():
    global INTERVAL
    count = 0
    score = 0
    game_over = False
    
    go_Next_Block(INTERVAL)
    set_Game_Field()
 
    while True:
        CLOCK.tick(10)
        SCREEN.fill(COLORS[0])
 
        key = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                key = event.key
            elif event.type == pg.KEYUP:
                key = None
 
        game_over = is_Game_Over()
        if not game_over:
            count += 5
            if count % 1000 == 0:
                INTERVAL = max(1, INTERVAL - 2)
            erased = BLOCK.update(count)
 
            if erased > 0:
                score += (2 ** erased) * 100
 
            # 키 이벤트 처리
            next_x, next_y, next_t = \
                BLOCK.xpos, BLOCK.ypos, BLOCK.turn
            if key == pg.K_UP:
                next_t = (next_t + 1) % 4
            elif key == pg.K_RIGHT:
                next_x += 1
            elif key == pg.K_LEFT:
                next_x -= 1
            elif key == pg.K_DOWN:
                next_y += 1
 
            if not is_Overlapped(next_x, next_y, next_t):
                BLOCK.xpos = next_x
                BLOCK.ypos = next_y
                BLOCK.turn = next_t
                BLOCK.data = BLOCK.type[BLOCK.turn]
 
        draw_Game_Field()
        draw_Current_Block()
        draw_Next_Block()
        #draw_score(score)
        if game_over:
            # draw_gameover_message()    
            pass
        pg.display.update()


if __name__ == "__main__":
    runGame()
    pg.quit()