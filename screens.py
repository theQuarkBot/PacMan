import pygame
from settings import *

class Button:
    def __init__(self, text, font_size, pos, bg=GREY):
        self.x, self.y = pos
        self.font = pygame.font.Font("bin/font/game over.ttf", font_size)
        self.text = text
        self.bg = bg
        self.render(self.text, self.bg)
    def render(self, text, bg):
        self.rendered = self.font.render(text, True, WHITE)
        self.size = self.rendered.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.rendered, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
    def show(self, scr):
        scr.blit(self.surface, (self.x, self.y))
    def hover_click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(x, y):
                self.render(self.text, RED)
            else:
                self.render(self.text, self.bg)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False
        

def startScreen(scr):
    width = scr.get_width() 
    height = scr.get_height() 

    fontTitle = pygame.font.Font("bin/font/game over.ttf", 120)
    fontText = pygame.font.Font("bin/font/game over.ttf", 30)

    pacman = fontTitle.render('Pac-Man', True, PELLET_COLOR)
    pacman_rect = pacman.get_rect(center=(width*0.52, height*0.4))

    enter = fontText.render('Click on mode to start', True, WHITE)
    enter_rect = enter.get_rect(center=(width*0.5, height*0.5))

    b1 = Button("1 Player", 50, (width*0.18, height*0.6))
    b2 = Button("2 Players", 50, (width*0.55, height*0.6))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
            #if event.type == pygame.KEYDOWN:
                #return
            if b1.hover_click(event):
                return 1
            if b2.hover_click(event):
                return 2

        scr.fill(BLACK)
        b1.show(scr)
        b2.show(scr)
        scr.blit(pacman, pacman_rect)
        scr.blit(enter, enter_rect)
        pygame.display.update() 

def gameOver(scr, board, winner="Ghost"):
    width = scr.get_width() 
    height = scr.get_height() 
    fontTitle = pygame.font.Font("bin/font/game over.ttf", 100)
    fontText = pygame.font.Font("bin/font/game over.ttf", 50)

    gameOver = fontTitle.render("Game Over", True, PELLET_COLOR)
    gameOver_rect = gameOver.get_rect(center=(width/2, height/2))

    win = fontText.render("Winner is the " + str(winner) + "!", True, PELLET_COLOR)
    win_rect = win.get_rect(center=(width/2, 4*height/7))

    #point = fontText.render("Pac-man got " + str(board.get_score()) + " out of "\
                             #+ str(MAX_SCORE) + " points" , True, WHITE)
    #point_rect = point.get_rect(center=(width/2, 4*height/7))
    text_bg = pygame.Rect(0, 0, width*0.8, height*0.2)
    text_bg.center = (width/2, height*0.53)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                return
        pygame.draw.rect(scr, BLACK, text_bg)
        scr.blit(gameOver, gameOver_rect)
        scr.blit(win, win_rect)
        pygame.display.update()