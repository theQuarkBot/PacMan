import pygame
from settings import *

def startScreen(scr):
    width = scr.get_width() 
    height = scr.get_height() 

    fontTitle = pygame.font.Font("bin/font/game over.ttf", 100)
    fontText = pygame.font.Font("bin/font/game over.ttf", 30)

    pacman = fontTitle.render('Pac-Man', True, PELLET_COLOR)
    pacman_rect = pacman.get_rect(center=(width/2, height/2))

    enter = fontText.render('Press Any Key to Start', True, WHITE)
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

    
def gameOver(scr, board):
    width = scr.get_width() 
    height = scr.get_height() 
    fontTitle = pygame.font.Font("bin/font/game over.ttf", 100)
    fontText = pygame.font.Font("bin/font/game over.ttf", 30)

    gameOver = fontTitle.render('Game Over', True, PELLET_COLOR)
    gameOver_rect = gameOver.get_rect(center=(width/2, height/2))

    point = fontText.render("Pac-man got " + str(board.get_score()) + " out of "\
                             + str(MAX_SCORE) + " points" , True, WHITE)
    point_rect = point.get_rect(center=(width/2, 4*height/7))
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
        scr.blit(point, point_rect)
        pygame.display.update()