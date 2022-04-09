import pygame  

# % - wall
# - - gate
# o - empty
# a - pellet
# s - super pellet
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

    def __init__(self, board, block_size=30, \
            wall_color=(0,0,255), pellet_color=(255, 255, 0)):
        self.board = board
        self.block_size = block_size
        self.wall_color = wall_color
        self.pellet_color = pellet_color

    def run(self):
        pygame.init()  
        bs = self.block_size
        scr = pygame.display.set_mode((len(self.board[0]) * bs, \
                                        len(self.board) * bs))  
        pygame.display.set_caption('Pac-Man')
        w_thick = 0.3 * bs
        bar_len = 0.5 * bs
        w_displ = 0.35 * bs

        i = 0
        for lines in self.board:
            j = 0
            for blocks in lines:
                if blocks == '%':
                    #draws center block
                    pygame.draw.rect(scr, self.wall_color, pygame.Rect(
                        j * bs + w_displ, 
                        i * bs + w_displ, 
                        w_thick, w_thick))
                    #draws upper bar if the box above is also wall 
                    #but the boxes left and right of itself and 
                    #left and right of box above are not all walls
                    if not (j != 0 and i != 0 and self.board[i-1][j-1] == '%' \
                        and self.board[i][j-1] == '%' \
                        and j != len(self.board[0])-1 \
                        and self.board[i-1][j+1] == '%' \
                        and self.board[i][j+1] == '%') \
                    and i != 0 and self.board[i-1][j] == '%':
                        pygame.draw.rect(scr, self.wall_color, \
                            pygame.Rect(j * bs + w_displ, i * bs, \
                                        w_thick, bar_len))

                    #draws bottom bar if the box below is also wall 
                    #but the boxes left and right of itself and 
                    #left and right of box below are not all walls
                    if not (j != 0 and i != len(self.board)-1 
                        and self.board[i+1][j-1] == '%' \
                        and self.board[i][j-1] == '%' \
                        and j != len(self.board[0])-1 \
                        and self.board[i+1][j+1] == '%' \
                        and self.board[i][j+1] == '%') \
                    and i != len(self.board)-1 and self.board[i+1][j] == '%':
                        pygame.draw.rect(scr, self.wall_color, \
                            pygame.Rect(j * bs + w_displ, i * bs + bar_len, \
                                        w_thick, bar_len))

                    #draws left bar if the box to left is also wall
                    if j != 0 and (self.board[i][j-1] == '%' \
                                    or self.board[i][j-1] == '-'):
                        pygame.draw.rect(scr, self.wall_color, \
                            pygame.Rect(j * bs, i * bs + w_displ, \
                                        bar_len, w_thick))

                    #draws right bar if the box to right is also wall
                    if j != len(self.board[0])-1 and \
                    (self.board[i][j+1] == '%' or self.board[i][j+1] == '-'):
                        pygame.draw.rect(scr, self.wall_color, \
                            pygame.Rect(j * bs + bar_len, i * bs + w_displ, \
                                        bar_len, w_thick))

                elif blocks == 'a':
                    pos = (j * bs + bs/2 , i * bs + bs/2)
                    pygame.draw.circle(scr, self.pellet_color, pos, bs/8)
                elif blocks == 's':
                    pos = (j * bs + bs/2 , i * bs + bs/2)
                    pygame.draw.circle(scr, self.pellet_color, pos, bs/4)
                elif blocks == '-':
                    pygame.draw.rect(scr, self.pellet_color, \
                        pygame.Rect(j * bs, i * bs + 0.45 * bs, bs, 0.1 * bs))
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


