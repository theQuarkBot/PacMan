#!/usr/bin/python3
import pygame
import threading
from thread_safe_classes import Lightswitch
from settings import *
from character_classes import Pacman, Ghost, RandomGhost
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

    pygame.mixer.init()
    pygame.mixer.music.load('bin/music/pacman.mp3')
    pygame.mixer.music.play(-1, 0.0)

    # Mutex and ligthswitch for update synchronization
    player_update_switch = Lightswitch()
    finished_updating = threading.Semaphore(1)

    # Generate pacman and all ghosts
    threads, pacmans, ghosts = generate_characters(
        board, player_num, player_update_switch, finished_updating)
    characters = pacmans + ghosts

    board.add_ghost_list(ghosts)

    # Run the game!
    winner = game_loop(characters, ghosts, pacmans, board, finished_updating,
        screen, clock, lives, winner)
    
    # Ensure all threads have stopped
    for thread in threads:
        thread.join()

    # Display game-over screen
    gameOver(screen, board, winner)

    pygame.quit()

    print("Thank you for playing!")


def game_loop(characters, ghosts, pacmans, board, finished_updating, screen,
              clock, lives, winner):
    running = True

    def stop_characters():
        for character in characters:
            character.stop()

    # Game loop
    while running:
        # End game with tie if user exits program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                winner = "Tie"
                stop_characters()

        # Check for any collisions; kill pacman or end game
        for ghost in ghosts:
            if pygame.sprite.spritecollideany(pacmans[0], [ghost]):
                if ghost.is_weak():
                    ghost.reset()
                    board.add_score(200)
                else:
                    board.minus_lives()
                    lives -= 1
                    if lives == 0:
                        winner = "Ghost"
                        running = False
                        stop_characters()

                    pygame.mixer.music.play(-1, 0.0)
                    #Respawn characters
                    pacmans[0].reset()
                    for ghost in ghosts:
                        ghost.reset()
            
        # Check for pacman win
        if board.check_if_no_pellet():
            winner = "Pac-Man"
            running = False
            stop_characters()

        # Ensure that all characters are not currently updating
        finished_updating.acquire()
        finished_updating.release()

        # Draw the board and the characters (non-concurrently)
        screen.fill((0, 0, 0))
        board.run()
        for character in characters:
            screen.blit(character.imageC, character.rect)
        pygame.display.flip()

        # Update the position of each character
        pressed_keys = pygame.key.get_pressed()
        for character in characters:
            character.update_event(pressed_keys)

        clock.tick(FPS)

    return winner


def generate_characters(board, player_num, player_update_switch, 
                                            finished_updating):
    # Make lists of threads and characters
    threads = []
    pacmans = []
    ghosts = []

    # Generate pacmans. Duplicate with appropriate controls for more
    pacman = Pacman(player_update_switch, finished_updating,
                        threads, board, PACMAN_START_POS, ARROW_CONTROLS)
    pacmans.append(pacman)

    # First ghost is player-controlled or computer controlled
    ghost1 = None
    if player_num == 2:
        ghost1 = Ghost(player_update_switch, finished_updating,
                       threads, board, GHOST_START_POS, WASD_CONTROLS)
        ghosts.append(ghost1)
    else:
        ghost1 = RandomGhost(player_update_switch, finished_updating,
                             threads, board, GHOST_START_POS)
        ghosts.append(ghost1)

    # Generate the rest of the ghosts
    ghost2 = RandomGhost(player_update_switch, finished_updating, threads,
                         board, GHOST_START_POS, None, GHOST_PINK)
    ghost3 = RandomGhost(player_update_switch, finished_updating, threads,
                         board, GHOST_START_POS, None, GHOST_ORANGE)
    ghost4 = RandomGhost(player_update_switch, finished_updating, threads,
                         board, GHOST_START_POS, None, GHOST_LIGHT_BLUE)

    ghosts.append(ghost2)
    ghosts.append(ghost3)
    ghosts.append(ghost4)

    return threads, pacmans, ghosts

if __name__ == '__main__':
    main()