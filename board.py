import pygame  

BOARD = [
    ['%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%'],
    ['%', 's', 'a', 'a', 'a', 'a', 'a', 'a', 'a', '%', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 's', '%'],
    ['%', 'a', '%', '%', 'a', '%', '%', '%', 'a', '%', 'a', '%', '%', '%', 'a', '%', '%', 'a', '%'],
    ['%', 'a', '%', '%', 'a', '%', '%', '%', 'a', '%', 'a', '%', '%', '%', 'a', '%', '%', 'a', '%'],
    ['%', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', '%'],
    ['%', 'a', '%', '%', 'a', '%', 'a', '%', '%', '%', '%', '%', 'a', '%', 'a', '%', '%', 'a', '%'],
    ['%', 'a', 'a', 'a', 's', '%', 'a', 'a', 'a', '%', 'a', 'a', 'a', '%', 's', 'a', 'a', 'a', '%'],
    ['%', '%', '%', '%', 'a', '%', '%', '%', 'a', '%', 'a', '%', '%', '%', 'a', '%', '%', '%', '%'],
    ['o', 'o', 'o', '%', 'a', '%', 'a', 'a', 'a', 'a', 'a', 'a', 'a', '%', 'a', '%', 'o', 'o', 'o'],
    ['%', '%', '%', '%', 'a', '%', 'a', '%', '%', '-', '%', '%', 'a', '%', 'a', '%', '%', '%', '%'],
    ['o', 'o', 'o', 'o', 'a', 'a', 'a', '%', 'o', 'o', 'o', '%', 'a', 'a', 'a', 'o', 'o', 'o', 'o'],
    ['%', '%', '%', '%', 'a', '%', 'a', '%', '%', '%', '%', '%', 'a', '%', 'a', '%', '%', '%', '%'],
    ['o', 'o', 'o', '%', 'a', '%', 'a', 'a', 'a', 'a', 'a', 'a', 'a', '%', 'a', '%', 'o', 'o', 'o'],
    ['%', '%', '%', '%', 'a', '%', '%', '%', 'a', '%', 'a', '%', '%', '%', 'a', '%', '%', '%', '%'],
    ['%', 'a', 'a', 'a', 's', '%', 'a', 'a', 'a', '%', 'a', 'a', 'a', '%', 's', 'a', 'a', 'a', '%'],
    ['%', 'a', '%', '%', 'a', '%', 'a', '%', '%', '%', '%', '%', 'a', '%', 'a', '%', '%', 'a', '%'],
    ['%', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', '%'],
    ['%', 'a', '%', '%', 'a', '%', '%', '%', 'a', '%', 'a', '%', '%', '%', 'a', '%', '%', 'a', '%'],
    ['%', 'a', '%', '%', 'a', '%', '%', '%', 'a', '%', 'a', '%', '%', '%', 'a', '%', '%', 'a', '%'],
    ['%', 's', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 's', '%'],
    ['%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%']

]

class Board():

    def __init__(self, board, block_size=30, wall_color=(0,0,255), pellet_color=(255, 255, 0)):
        self.board = board
        self.block_size = block_size
        self.wall_color = wall_color
        self.pellet_color = pellet_color

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
                elif blocks == 'a':
                    pos = (j * self.block_size + self.block_size/2 , i * self.block_size + self.block_size/2)
                    pygame.draw.circle(scr, self.pellet_color, pos, self.block_size/8)
                elif blocks == 's':
                    pos = (j * self.block_size + self.block_size/2 , i * self.block_size + self.block_size/2)
                    pygame.draw.circle(scr, self.pellet_color, pos, self.block_size/4)
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


