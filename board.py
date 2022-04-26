import pygame  
from settings import *

# % - wall
# - - gate
# o - empty
# a - pellet
# s - super pellet
BOARD = [
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
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
    ['%', '%', '%', '%', 'a', '%', 'a', 'a', 'a', '%', 'a', 'a', 'a', '%', 'a', '%', '%', '%', '%'],
    ['%', 'a', 'a', 'a', 's', '%', 'a', 'a', 'a', '%', 'a', 'a', 'a', '%', 's', 'a', 'a', 'a', '%'],
    ['%', 'a', '%', '%', 'a', '%', 'a', '%', '%', '%', '%', '%', 'a', '%', 'a', '%', '%', 'a', '%'],
    ['%', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'o', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', '%'],
    ['%', 'a', '%', '%', 'a', '%', '%', '%', 'a', '%', 'a', '%', '%', '%', 'a', '%', '%', 'a', '%'],
    ['%', 'a', '%', '%', 'a', '%', '%', '%', 'a', '%', 'a', '%', '%', '%', 'a', '%', '%', 'a', '%'],
    ['%', 's', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 's', '%'],
    ['%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%']
]

class Board():

    def __init__(self, scr, board=BOARD, block_size=BLOCKSIZE, \
            wall_color=WALL_COLOR, pellet_color=PELLET_COLOR):
        self.scr = scr
        self.board = board
        self.block_size = block_size
        self.wall_color = wall_color
        self.pellet_color = pellet_color
        self.score = 0
        self.blink = 0
        self.lives = START_LIVES

    def minus_lives(self):
        self.lives -= 1
        
    def get_score(self):
        return self.score
        
    def check_wall(self, rect):
        top_left     = self.board \
                        [int((rect.top    + 1) / self.block_size)] \
                        [int((rect.left   + 1) / self.block_size)]
        bottom_left  = self.board \
                        [int((rect.bottom - 1) / self.block_size)] \
                        [int((rect.left   + 1) / self.block_size)]
        top_right    = self.board \
                        [int((rect.top    + 1) / self.block_size)] \
                        [int((rect.right  - 1) / self.block_size)]
        bottom_right = self.board \
                        [int((rect.bottom - 1) / self.block_size)] \
                        [int((rect.right  - 1) / self.block_size)]

        # Check if colliding with wall
        if top_left == '%' or bottom_left == '%' or \
           top_right == '%' or bottom_right == '%':
            return False
        return True

    def check_wall_rand_ghost(self, rect, dirc):
        top_left     = self.board \
                        [int((rect.top    + 1) / self.block_size)] \
                        [int((rect.left   + 1) / self.block_size)]
        bottom_left  = self.board \
                        [int((rect.bottom - 1) / self.block_size)] \
                        [int((rect.left   + 1) / self.block_size)]
        top_right    = self.board \
                        [int((rect.top    + 1) / self.block_size)] \
                        [int((rect.right  - 1) / self.block_size)]
        bottom_right = self.board \
                        [int((rect.bottom - 1) / self.block_size)] \
                        [int((rect.right  - 1) / self.block_size)]

        if top_left == '-' or bottom_left in '-' or \
           top_right == '-' or bottom_right in '-':
            if dirc == 1:
                return False

        # Check if colliding with wall
        if top_left == '%' or bottom_left in '%' or \
           top_right == '%' or bottom_right in '%':
            return False
        return True

    def check_pellet(self, rect):
        offset = self.block_size/2
        top_left     = (int((rect.top    + offset) / self.block_size), \
                        int((rect.left   + offset) / self.block_size))
        bottom_left  = (int((rect.bottom - offset) / self.block_size), \
                        int((rect.left   + offset) / self.block_size))
        top_right    = (int((rect.top    + offset) / self.block_size), \
                        int((rect.right  - offset) / self.block_size))
        bottom_right = (int((rect.bottom - offset) / self.block_size), \
                        int((rect.right  - offset) / self.block_size))

        # Remove pellet if going over pellet
        if self.board[top_left[0]][top_left[1]] == 'a':
            self.board[top_left[0]][top_left[1]] = 'o'
            self.score += 1
        if self.board[bottom_left[0]][bottom_left[1]] == 'a':
            self.board[bottom_left[0]][bottom_left[1]] = 'o'
            self.score += 1
        if self.board[top_right[0]][top_right[1]] == 'a':
            self.board[top_right[0]][top_right[1]] = 'o'
            self.score += 1
        if self.board[bottom_right[0]][bottom_right[1]] == 'a':
            self.board[bottom_right[0]][bottom_right[1]] = 'o'
            self.score += 1

        if self.board[top_left[0]][top_left[1]] == 's':
            self.board[top_left[0]][top_left[1]] = 'o'
            self.score += 5
        if self.board[bottom_left[0]][bottom_left[1]] == 's':
            self.board[bottom_left[0]][bottom_left[1]] = 'o'
            self.score += 5
        if self.board[top_right[0]][top_right[1]] == 's':
            self.board[top_right[0]][top_right[1]] = 'o'
            self.score += 5
        if self.board[bottom_right[0]][bottom_right[1]] == 's':
            self.board[bottom_right[0]][bottom_right[1]] = 'o'
            self.score += 5

    def run(self):

        bs = self.block_size
        scr = self.scr
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
                    #but the boxes up and down of itself and
                    #up and down of box to the right are not all walls
                    if not (j != 0 and i != 0 and self.board[i-1][j-1] == '%' \
                        and self.board[i-1][j] in '%' \
                        and i != len(self.board)-1 \
                        and self.board[i+1][j-1] == '%' \
                        and self.board[i+1][j] == '%') \
                    and j != 0 and self.board[i][j-1] in ('%', '-'):
                        pygame.draw.rect(scr, self.wall_color, \
                            pygame.Rect(j * bs, i * bs + w_displ, \
                                        bar_len, w_thick))

                    #draws right bar if the box to right is also wall
                    #but the boxes up and down of itself and
                    #up and down of box to the left are not all walls
                    if not (i != 0 and j != len(self.board[0])-1
                        and self.board[i-1][j+1] == '%' \
                        and self.board[i-1][j] == '%' \
                        and i != len(self.board)-1 \
                        and self.board[i+1][j+1] == '%' \
                        and self.board[i+1][j] == '%') \
                    and j != len(self.board[0])-1 and self.board[i][j+1] in ('%', '-'):
                        pygame.draw.rect(scr, self.wall_color, \
                            pygame.Rect(j * bs + bar_len, i * bs + w_displ, \
                                        bar_len, w_thick))

                elif blocks == 'a':
                    pos = (j * bs + bs/2 , i * bs + bs/2)
                    pygame.draw.circle(scr, self.pellet_color, pos, bs/8)
                elif blocks == 's':
                    if self.blink > 15:
                        pos = (j * bs + bs/2 , i * bs + bs/2)
                        pygame.draw.circle(scr, self.pellet_color, pos, bs/4)
                elif blocks == '-':
                    pygame.draw.rect(scr, self.pellet_color, \
                        pygame.Rect(j * bs, i * bs + 0.45 * bs, bs, 0.1 * bs))
                j += 1
            i += 1
        if self.blink == 30:
            self.blink = 0
        self.blink += 1
        font = pygame.font.Font("bin/font/game over.ttf", 36)
        score_text = font.render("Score: "+str(self.score)+"/"+str(MAX_SCORE),\
                                    True, RED)
        scr.blit(score_text, [10, 10])
        lives_text = font.render("Lives: "+str(self.lives), True, RED)
        scr.blit(lives_text, \
                    [scr.get_width() - lives_text.get_size()[0] - 10, 10])
if __name__ == '__main__':
    b = Board()
    b.run()


