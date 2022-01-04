import pygame as pg
import time, sys


PIECE_SIZE = 24
PIECE_GRID_SIZE = PIECE_SIZE + 1
BOARD_WIDTH = 14
BOARD_HEIGHT = 21
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
BOARD = []
COLORS = ((0, 0, 0), (255, 165, 0), (0, 0, 255), (0, 255, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 0, 0), (128, 128, 128))

CLOCK = pg.time.Clock()

class Tetris(object):
    def __init__(self):
        pg.init()
        pg.display.set_caption("Tetris")
        self.screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) 
    
    def setBoard(self):
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
        for i in range(BOARD_HEIGHT):
            print(BOARD[i])
            
    def printBoard(self):
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                board = BOARD[i][j]
                color = COLORS[board]
                pg.draw.rect(self.screen,color,(PIECE_GRID_SIZE + j*PIECE_GRID_SIZE, 
                            PIECE_GRID_SIZE + i*PIECE_GRID_SIZE , 
                            PIECE_SIZE , 
                            PIECE_SIZE ))
    
    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            else:
                pass
    
    def start(self):
        self.setBoard()
        while True:
            CLOCK.tick(10)
            self.printBoard()
            self.event()
            pg.display.update()


if __name__ == "__main__":
    game = Tetris()
    game.start()