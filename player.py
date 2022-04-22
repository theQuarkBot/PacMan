#!/usr/bin/python3

from distutils.dep_util import newer
import os, sys, random
import pygame
import threading
from settings import *
from thread_safe_classes import Lightswitch
from board import Board

class PacmanTesting:
    def __init__(self, controls, update_switch, finished_updating, all_threads,\
                 board, start_pos):
        # Initialize sprite image
        self.__init_sprites__()
        self.imageC = self.imageR
        self.imageN = self.imageC
        self.rect = self.imageC.get_rect()

        self.board = board
        self.rect.topleft = start_pos

        # Initialize movement buffer
        self.cur_vector = pygame.Vector2((0, 0))
        self.next_vector = pygame.Vector2((0, 0))

        # Set controls
        (self.UP, self.DOWN, self.LEFT, self.RIGHT) = controls

        # Update synchronization variables
        self.can_update = threading.Semaphore(0)
        self.update_switch = update_switch
        self.finished_updating = finished_updating
        self.mutex = threading.Semaphore(1)

        self.running = True

        # Start movement thread
        self.thread = threading.Thread(target=self.__run__)
        all_threads.append(self.thread)
        self.thread.start()

    def __init_sprites__(self):
        self.imageU = pygame.image.load(
            "bin/sprites/pacman-u-4.gif").convert_alpha()
        self.imageD = pygame.image.load(
            "bin/sprites/pacman-d-4.gif").convert_alpha()
        self.imageL = pygame.image.load(
            "bin/sprites/pacman-l-4.gif").convert_alpha()
        self.imageR = pygame.image.load(
            "bin/sprites/pacman-r-4.gif").convert_alpha()

        self.__sprite_dimensions__ = (BLOCKSIZE, BLOCKSIZE)
        
        self.imageU = pygame.transform.scale(
            self.imageU, self.__sprite_dimensions__)
        self.imageD = pygame.transform.scale(
            self.imageD, self.__sprite_dimensions__)
        self.imageL = pygame.transform.scale(
            self.imageL, self.__sprite_dimensions__)
        self.imageR = pygame.transform.scale(
            self.imageR, self.__sprite_dimensions__)

    def update_event(self, pressed_keys):
        self.update_switch.lock(self.finished_updating)

        self.pressed_keys = pressed_keys

        self.can_update.release()

    def __run__(self):
        while self.running:
            self.can_update.acquire()
            self.__update_pos__()

    def stop(self):
        self.running = False
        # while self.thread.is_alive():
        self.can_update.release()

    def __update_pos__(self):
        # Save the keypresses and next image for next velocity change
        if self.pressed_keys[self.UP]:
            self.next_vector.xy = 0, -PACMAN_SPEED
            self.imageN = self.imageU
        elif self.pressed_keys[self.DOWN]:
            self.next_vector.xy = 0, PACMAN_SPEED
            self.imageN = self.imageD
        elif self.pressed_keys[self.LEFT]:
            self.next_vector.xy = -PACMAN_SPEED, 0
            self.imageN = self.imageL
        elif self.pressed_keys[self.RIGHT]:
            self.next_vector.xy = PACMAN_SPEED, 0
            self.imageN = self.imageR

        # Determine whether it can go in the new direction
        new_rect = self.rect.move(self.next_vector.x, self.next_vector.y)
        self.__try_teleport_through_tunnel__(new_rect)
        can_move = self.board.check_wall(new_rect)

        # Update the current move if the new move is possible
        if can_move:
            self.cur_vector.xy = self.next_vector.xy
            self.imageC = self.imageN
        # Otherwise try moving in the old direction
        else: 
            new_rect = self.rect.move(self.cur_vector.x, self.cur_vector.y)
            self.__try_teleport_through_tunnel__(new_rect)
            can_move = self.board.check_wall(new_rect)

        # Update position
        if can_move:
            self.board.check_pellet(new_rect)
            self.rect.topleft = new_rect.topleft

        self.update_switch.unlock(self.finished_updating)

    def __try_teleport_through_tunnel__(self, rect):
        if rect.left < 0:
            rect.right = WIDTH - 2
        if rect.right >= WIDTH:
            rect.left = 0
        if rect.top <= 0:
            rect.bottom = HEIGHT - 2
        if rect.bottom >= HEIGHT:
            rect.top = 0


class GhostTesting:
    def __init__(self, controls, update_switch, finished_updating, all_threads,
                 board, start_pos):
        # Initialize sprite image
        self.__init_sprites__()
        self.imageC = self.imageR
        self.imageN = self.imageC
        self.rect = self.imageC.get_rect()

        self.board = board
        self.rect.topleft = start_pos

        # Initialize movement buffer
        self.cur_vector = pygame.Vector2((0, 0))
        self.next_vector = pygame.Vector2((0, 0))

        # Set controls
        (self.UP, self.DOWN, self.LEFT, self.RIGHT) = controls

        # Update synchronization variables
        self.can_update = threading.Semaphore(0)
        self.update_switch = update_switch
        self.finished_updating = finished_updating
        self.mutex = threading.Semaphore(1)

        self.running = True

        # Start movement thread
        self.thread = threading.Thread(target=self.__run__)
        all_threads.append(self.thread)
        self.thread.start()

    def __init_sprites__(self):
        self.imageU = pygame.image.load(
            "bin/sprites/ghost-4.gif").convert_alpha()
        self.imageD = self.imageU
        self.imageL = self.imageU
        self.imageR = self.imageU

        self.__sprite_dimensions__ = (BLOCKSIZE, BLOCKSIZE)

        self.imageU = pygame.transform.scale(
            self.imageU, self.__sprite_dimensions__)
        self.imageD = pygame.transform.scale(
            self.imageD, self.__sprite_dimensions__)
        self.imageL = pygame.transform.scale(
            self.imageL, self.__sprite_dimensions__)
        self.imageR = pygame.transform.scale(
            self.imageR, self.__sprite_dimensions__)

    def update_event(self, pressed_keys):
        self.update_switch.lock(self.finished_updating)

        self.pressed_keys = pressed_keys

        self.can_update.release()

    def __run__(self):
        while self.running:
            self.can_update.acquire()
            self.__update_pos__()

    def stop(self):
        self.running = False
        # while self.thread.is_alive():
        self.can_update.release()

    def __update_pos__(self):
        # Save the keypresses and next image for next velocity change
        if self.pressed_keys[self.UP]:
            self.next_vector.xy = 0, -PACMAN_SPEED
            self.imageN = self.imageU
        elif self.pressed_keys[self.DOWN]:
            self.next_vector.xy = 0, PACMAN_SPEED
            self.imageN = self.imageD
        elif self.pressed_keys[self.LEFT]:
            self.next_vector.xy = -PACMAN_SPEED, 0
            self.imageN = self.imageL
        elif self.pressed_keys[self.RIGHT]:
            self.next_vector.xy = PACMAN_SPEED, 0
            self.imageN = self.imageR

        # Determine whether it can go in the new direction
        new_rect = self.rect.move(self.next_vector.x, self.next_vector.y)
        self.__try_teleport_through_tunnel__(new_rect)
        can_move = self.board.check_wall(new_rect)

        # Update the current move if the new move is possible
        if can_move:
            self.cur_vector.xy = self.next_vector.xy
            self.imageC = self.imageN
        # Otherwise try moving in the old direction
        else:
            new_rect = self.rect.move(self.cur_vector.x, self.cur_vector.y)
            self.__try_teleport_through_tunnel__(new_rect)
            can_move = self.board.check_wall(new_rect)

        # Update position
        if can_move:
            self.rect.topleft = new_rect.topleft

        self.update_switch.unlock(self.finished_updating)

    def __try_teleport_through_tunnel__(self, rect):
        if rect.left < 0:
            rect.right = WIDTH - 2
        if rect.right >= WIDTH:
            rect.left = 0
        if rect.top <= 0:
            rect.bottom = HEIGHT - 2
        if rect.bottom >= HEIGHT:
            rect.top = 0


def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    player_update_switch = Lightswitch()
    finished_updating = threading.Semaphore(1)

    threads = []
    players = []

    player1 = Pacman(ARROW_CONTROLS, player_update_switch, finished_updating, threads)
    players.append(player1)

    player2 = Pacman(WASD_CONTROLS, player_update_switch, finished_updating, threads)
    players.append(player2)

    running = True

    while running:
        # Game end events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

                for player in players:
                    player.stop()

        finished_updating.acquire()
        finished_updating.release()

        screen.fill((0, 0, 0))

        for player in players:
            screen.blit(player.imageC, player.rect)

        pygame.display.flip()

        pressed_keys = pygame.key.get_pressed()

        for player in players:
            player.update_event(pressed_keys)

        clock.tick(FPS)
    pygame.quit()

    for thread in threads:
        thread.join()

    print("Thank you for playing!")

if __name__ == "__main__":
    main()