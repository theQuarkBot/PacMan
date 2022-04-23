import pygame
from settings import *

def startScreen(scr):
    width = scr.get_width() 
    height = scr.get_height() 

    fontTitle = pygame.font.Font("bin/font/game over.ttf", 100)
    fontEnter = pygame.font.Font("bin/font/game over.ttf", 30)

    pacman = fontTitle.render('Pac-Man', True, PELLET_COLOR)
    pacman_rect = pacman.get_rect(center=(width/2, height/2))

    enter = fontEnter.render('Press Enter to Start', True, WHITE)
    enter_rect = enter.get_rect(center=(width/2, 4*height/7))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
            if event.type == pygame.KEYDOWN:
                return
        scr.fill(BLACK)
        scr.blit(pacman, pacman_rect)
        scr.blit(enter, enter_rect)
        pygame.display.update() 

    
def gameOver(scr):
    width = scr.get_width() 
    height = scr.get_height() 
