import pygame  
from settings import *

class Board():

    def __init__(self, scr, board=BOARD, block_size=BLOCKSIZE, \
            wall_color=WALL_COLOR, pellet_color=PELLET_COLOR):
        """ Init a board with default of spec in settings.py """
        self.scr = scr
        self.board = board
        self.block_size = block_size
        self.wall_color = wall_color
        self.pellet_color = pellet_color
        self.score = 0
        self.blink = 0
        self.lives = START_LIVES
        self.pellet = PELLET_NUM

    def add_ghost_list(self, ghosts):
        """ Store list of ghosts """
        self.ghosts = ghosts

    def all_ghosts_weak(self):
        """ Turn all ghosts into weak state """
        for ghost in self.ghosts:
            ghost.set_weak()

    def check_if_no_pellet(self):
        """ Return True if pellet is 0 """
        if self.pellet == 0:
            return True
        return False

    def minus_lives(self):
        """ Decrement a life """
        self.lives -= 1

    def add_score(self, score):
        """ Increment score by the given value """
        self.score += score
        
    def get_score(self):
        """ Get pac-man's pellet score """
        return self.score

    def get_block(self, coord):
        """ Get the symbol at given coord """
        return self.board[coord[0]][coord[1]]

    def put_block(self, coord, v):
        """ Change the symbol to v at given coord """
        self.board[coord[0]][coord[1]] = v

    def check_wall(self, rect):
        """ Check if colliding with wall """
        (top_left, bottom_left, top_right, bottom_right) = \
                                            self.get_corners(rect, 0.5)

        if self.get_block(top_left) == '%' \
        or self.get_block(bottom_left) in '%' \
        or self.get_block(top_right) == '%' \
        or self.get_block(bottom_right) in '%':
            return False
        return True

    def check_wall_rand_ghost(self, rect, dirc):
        """ Check if colliding with wall for random ghosts, one-way gate """
        (top_left, bottom_left, top_right, bottom_right) = \
                                            self.get_corners(rect, 0.5)
        # Check if going down into gate

        if self.get_block(top_left) == '-' \
        or self.get_block(bottom_left) in '-' \
        or self.get_block(top_right) == '-' \
        or self.get_block(bottom_right) in '-':
            if dirc == 1:
                return False

        # Check if colliding with wall

        if self.get_block(top_left) == '%' \
        or self.get_block(bottom_left) in '%' \
        or self.get_block(top_right) == '%' \
        or self.get_block(bottom_right) in '%':
            return False
        return True

    def check_pellet(self, rect):
        """ Check if touched pellet and add points accordingly """
        offset = self.block_size/2
        (top_left, bottom_left, top_right, bottom_right) = \
                                self.get_corners(rect, self.block_size/2)

        # Remove pellet if going over pellet

        if self.get_block(top_left) == 'a':
            self.put_block(top_left, 'o')
            self.pellet -= 1
            self.score += 10
        if self.get_block(bottom_left) == 'a':
            self.put_block(bottom_left, 'o')
            self.pellet -= 1
            self.score += 10
        if self.get_block(top_right) == 'a':
            self.put_block(top_right, 'o')
            self.pellet -= 1
            self.score += 10
        if self.get_block(bottom_right) == 'a':
            self.put_block(bottom_right, 'o')
            self.pellet -= 1
            self.score += 10

        if self.get_block(top_left) == 's':
            self.all_ghosts_weak()
            self.put_block(top_left, 'o')
            self.pellet -= 1
            self.score += 50
        if self.get_block(bottom_left) == 's':
            self.all_ghosts_weak()
            self.put_block(bottom_left, 'o')
            self.pellet -= 1
            self.score += 50
        if self.get_block(top_right) == 's':
            self.all_ghosts_weak()
            self.put_block(top_right, 'o')
            self.pellet -= 1
            self.score += 50
        if self.get_block(bottom_right) == 's':
            self.all_ghosts_weak()
            self.put_block(bottom_right, 'o')
            self.pellet -= 1
            self.score += 50

    def get_corners(self, rect, offset):
        """ Helper function for the check functions, get the block of the four corners """
        top_left     = (int((rect.top    + offset) / self.block_size), \
                        int((rect.left   + offset) / self.block_size))
        bottom_left  = (int((rect.bottom - offset) / self.block_size), \
                        int((rect.left   + offset) / self.block_size))
        top_right    = (int((rect.top    + offset) / self.block_size), \
                        int((rect.right  - offset) / self.block_size))
        bottom_right = (int((rect.bottom - offset) / self.block_size), \
                        int((rect.right  - offset) / self.block_size))

        return (top_left, bottom_left, top_right, bottom_right)

    def run(self):
        """ Draws the board """
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
                    and j != len(self.board[0])-1 \
                    and self.board[i][j+1] in ('%', '-'):
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

        #Super pellets are shown on and off every 30 frames
        if self.blink == 30:
            self.blink = 0
        self.blink += 1

        #Display score and lives
        font = pygame.font.Font("bin/font/game over.ttf", 36)

        score_text = font.render("Score: "+str(self.score),\
                                    True, RED)
        scr.blit(score_text, [10, 10])

        lives_text = font.render("Lives: "+str(self.lives), True, RED)
        scr.blit(lives_text, \
                    [scr.get_width() - lives_text.get_size()[0] - 10, 10])
if __name__ == '__main__':
    b = Board()
    b.run()


