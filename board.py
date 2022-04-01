import pygame  

BOARD = [
    ['%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%'],
    ['%', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '%', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '%'],
    ['%', 'o', '%', '%', 'o', '%', '%', '%', 'o', '%', 'o', '%', '%', '%', 'o', '%', '%', 'o', '%'],
    ['%', 'o', '%', '%', 'o', '%', '%', '%', 'o', '%', 'o', '%', '%', '%', 'o', '%', '%', 'o', '%'],
    ['%', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '%'],
    ['%', 'o', '%', '%', 'o', '%', 'o', '%', '%', '%', '%', '%', 'o', '%', 'o', '%', '%', 'o', '%'],
    ['%', 'o', 'o', 'o', 'o', '%', 'o', 'o', 'o', '%', 'o', 'o', 'o', '%', 'o', 'o', 'o', 'o', '%'],
    ['%', '%', '%', '%', 'o', '%', '%', '%', 'o', '%', 'o', '%', '%', '%', 'o', '%', '%', '%', '%'],
    ['o', 'o', 'o', '%', 'o', '%', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '%', 'o', '%', 'o', 'o', 'o'],
    ['%', '%', '%', '%', 'o', '%', 'o', '%', '%', '-', '%', '%', 'o', '%', 'o', '%', '%', '%', '%'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', '%', 'o', 'o', 'o', '%', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['%', '%', '%', '%', 'o', '%', 'o', '%', '%', '%', '%', '%', 'o', '%', 'o', '%', '%', '%', '%'],
    ['o', 'o', 'o', '%', 'o', '%', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '%', 'o', '%', 'o', 'o', 'o'],
    ['%', '%', '%', '%', 'o', '%', '%', '%', 'o', '%', 'o', '%', '%', '%', 'o', '%', '%', '%', '%'],
    ['%', 'o', 'o', 'o', 'o', '%', 'o', 'o', 'o', '%', 'o', 'o', 'o', '%', 'o', 'o', 'o', 'o', '%'],
    ['%', 'o', '%', '%', 'o', '%', 'o', '%', '%', '%', '%', '%', 'o', '%', 'o', '%', '%', 'o', '%'],
    ['%', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '%'],
    ['%', 'o', '%', '%', 'o', '%', '%', '%', 'o', '%', 'o', '%', '%', '%', 'o', '%', '%', 'o', '%'],
    ['%', 'o', '%', '%', 'o', '%', '%', '%', 'o', '%', 'o', '%', '%', '%', 'o', '%', '%', 'o', '%'],
    ['%', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '%'],
    ['%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%']

]

class Board():

    def __init__(self, board, block_size=30, wall_color=(0,0,255)):
        self.board = board
        self.block_size = block_size
        self.wall_color = wall_color

    def run(self):
        pygame.init()  
        scr = pygame.display.set_mode((len(self.board[0]) * self.block_size, len(self.board) * self.block_size))  
        pygame.display.set_caption('Pac-Man')
        i = 0
        for lines in self.board:
            j = 0
            for blocks in lines:
                if blocks == '%':
                    pygame.draw.rect(scr, self.wall_color, pygame.Rect(j * self.block_size, i * self.block_size, self.block_size, self.block_size))
                j += 1
            i += 1

        pygame.display.flip()  

        running = True
        while running: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    running = False
        pygame.quit() 

if __name__ == '__main__':
    b = Board(BOARD)
    b.run()


