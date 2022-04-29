#!/usr/bin/python3
import pygame
import threading
from thread_safe_classes import Lightswitch
from settings import *
from pacman_class import Pacman, Ghost, RandomGhost
from board import Board
from screens import *

def main():
    pygame.init()
    pygame.font.init()

    pygame.display.set_caption('Pac-Man')

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    player_num = startScreen(screen)

    winner = "Tie"

    board = Board(screen)
    lives = START_LIVES

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
    pacman1 = Pacman(player_update_switch, finished_updating, 
                     threads, board, PACMAN_START_POS, ARROW_CONTROLS)
    ghost2 = RandomGhost(player_update_switch, finished_updating,
                         threads, board, GHOST_START_POS, None, GHOST_PINK)
    ghost3 = RandomGhost(player_update_switch, finished_updating,
                         threads, board, GHOST_START_POS, None, GHOST_ORANGE)
    ghost4 = RandomGhost(player_update_switch, finished_updating,
                         threads, board, GHOST_START_POS, None, GHOST_LIGHT_BLUE)

    pacmans.append(pacman1)
    ghosts.append(ghost2)
    ghosts.append(ghost3)
    ghosts.append(ghost4)

    if player_num == 2:
        ghost1 = Ghost(player_update_switch, finished_updating, 
                       threads, board, GHOST_START_POS, WASD_CONTROLS)
        ghosts.append(ghost1)
    else:
        ghost5 = RandomGhost(player_update_switch,
                      finished_updating, threads, board, None, GHOST_START_POS)
        ghosts.append(ghost5)

    board.add_ghost_list(ghosts)
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

        for ghost in ghosts:
            if pygame.sprite.spritecollideany(pacmans[0], [ghost]):
                if ghost.is_weak():
                    ghost.reset()
                    board.add_score(200)
                else:
                    board.minus_lives()
                    lives -= 1
                    if not lives:
                        winner = "Ghost"
                        running = False
                        for player in players:
                            player.stop()
                    #Respawn players
                    pacmans[0].reset()
                    for g in ghosts:
                        g.reset()
            
        if board.check_if_no_pellet():
            winner = "Pac-Man"
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
    gameOver(screen, board, winner)
    pygame.quit()

    for thread in threads:
        thread.join()

    print("Thank you for playing!")

if __name__ == '__main__':
    main()