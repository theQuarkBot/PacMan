#!/usr/bin/python3
import pygame
import threading
from thread_safe_classes import Lightswitch
from settings import *
from pacman_class import Pacman, Ghost
from board import Board
from player import PacmanTesting, GhostTesting

def main():
    pygame.init()
    pygame.display.set_caption('Pac-Man')

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    
    board = Board(screen)

    # Mutex and ligthswitch to support 
    player_update_switch = Lightswitch()
    finished_updating = threading.Semaphore(1)


    # Create a list of players
    threads = []
    pacmans = []
    ghosts = []

    players = []

    #The Start positions are not used currently
    # pacman1 = PacmanTesting(ARROW_CONTROLS, player_update_switch,
    #                  finished_updating, threads, board, PACMAN_START_POS)
    # ghost1 = GhostTesting(WASD_CONTROLS, player_update_switch,
    #                   finished_updating, threads, board, GHOST_START_POS)
    pacman1 = Pacman(ARROW_CONTROLS, player_update_switch,
                     finished_updating, threads, board, PACMAN_START_POS)
    ghost1 = Ghost(WASD_CONTROLS, player_update_switch,
                      finished_updating, threads, board, GHOST_START_POS)
    pacmans.append(pacman1)
    ghosts.append(ghost1)

    players = pacmans + ghosts

    running = True

    # Game loop
    while running:
        # Game end events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

                for player in players:
                    player.stop()
        if pygame.sprite.spritecollideany(pacmans[0], ghosts):
            running = False
            for player in players:
                    player.stop()

        # Ensure that all players are not currently updating
        finished_updating.acquire()
        finished_updating.release()

        # Draw the board and the players (non-concurrently)
        screen.fill((0, 0, 0))
        board.run()
        for player in players:
            screen.blit(player.imageC, player.rect)
        pygame.display.flip()

        # Update the position of each player
        pressed_keys = pygame.key.get_pressed()
        for player in players:
            player.update_event(pressed_keys)

        clock.tick(FPS)
    pygame.quit()

    for thread in threads:
        thread.join()

    print("Thank you for playing!")

if __name__ == '__main__':
    main()