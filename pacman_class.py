#!/usr/bin/python3

from distutils.dep_util import newer
import os, sys, random
import pygame
import threading
from settings import *
from thread_safe_classes import Lightswitch
from board import Board


class Pacman:
    def __init__(self, controls, update_switch, finished_updating, all_threads,\
                 board, start_pos):
        # Initialize sprite image
        self.__init_sprites__()
        self.imageC = self.imageR
        self.rect = self.imageC.get_rect()

        self.board = board
        self.rect.topleft = (9 * BLOCKSIZE, 17 * BLOCKSIZE) #start_pos

        (self.UP, self.DOWN, self.LEFT, self.RIGHT) = controls

        self.can_update = threading.Semaphore(0)
        self.update_switch = update_switch
        self.finished_updating = finished_updating

        self.mutex = threading.Semaphore(1)
        self.running = True

        self.thread = threading.Thread(target=self.__run__)
        all_threads.append(self.thread)
        self.thread.start()

    def __init_sprites__(self):
        self.imageU = pygame.image.load(
            "bin/large_sprites/pac_up.png").convert_alpha()
        self.imageD = pygame.image.load(
            "bin/large_sprites/pac_down.png").convert_alpha()
        self.imageL = pygame.image.load(
            "bin/large_sprites/pac_left.png").convert_alpha()
        self.imageR = pygame.image.load(
            "bin/large_sprites/pac_right.png").convert_alpha()

        self.size = self.imageU.get_size()
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
        new_vector = (0, 0)
        if self.pressed_keys[self.UP]:
            new_vector = (0, -PACMAN_SPEED)
            self.imageC = self.imageU
        elif self.pressed_keys[self.DOWN]:
            new_vector = (0, PACMAN_SPEED)
            self.imageC = self.imageD
        elif self.pressed_keys[self.LEFT]:
            new_vector = (-PACMAN_SPEED, 0)
            self.imageC = self.imageL
        elif self.pressed_keys[self.RIGHT]:
            new_vector = (PACMAN_SPEED, 0)
            self.imageC = self.imageR
 
        new_rect = self.rect.move(new_vector[0], new_vector[1])
        
        # Check if rect is in moveable area
            # Yes -> update pos
            # No -> Don't update( and stop?)

        can_move = self.board.check_wall(new_rect)
        self.board.check_pellet(new_rect)
        
        if can_move:
            #print(new_vector)
            self.rect.move_ip(new_vector[0], new_vector[1])

        # # Change position according to key_press
        # if self.pressed_keys[self.UP]:
        #     self.rect.move_ip(0, -PACMAN_SPEED)
        #     self.imageC = self.imageU
        # elif self.pressed_keys[self.DOWN]:
        #     self.rect.move_ip(0, PACMAN_SPEED)
        #     self.imageC = self.imageD
        # elif self.pressed_keys[self.LEFT]:
        #     self.rect.move_ip(-PACMAN_SPEED, 0)
        #     self.imageC = self.imageL
        # elif self.pressed_keys[self.RIGHT]:
        #     self.rect.move_ip(PACMAN_SPEED, 0)
        #     self.imageC = self.imageR

        # Ensure pacman stays in bounds.
        if new_rect.left < 0:
            new_rect.left = 0
        if new_rect.right > WIDTH:
            new_rect.right = WIDTH
        if new_rect.top <= 0:
            new_rect.top = 0
        if new_rect.bottom >= HEIGHT:
            new_rect.bottom = HEIGHT

        # self.rect = new_rect

        self.update_switch.unlock(self.finished_updating)


class Ghost:
    def __init__(self, controls, update_switch, finished_updating, all_threads,\
                 board, start_pos):
        # Initialize sprite image
        self.__init_sprites__()
        self.imageC = self.imageR
        self.rect = self.imageC.get_rect()

        self.board = board
        self.rect.topleft = (9 * BLOCKSIZE, 11 * BLOCKSIZE) #start_pos

        (self.UP, self.DOWN, self.LEFT, self.RIGHT) = controls

        self.can_update = threading.Semaphore(0)
        self.update_switch = update_switch
        self.finished_updating = finished_updating

        self.mutex = threading.Semaphore(1)
        self.running = True

        self.thread = threading.Thread(target=self.__run__)
        all_threads.append(self.thread)
        self.thread.start()

    def __init_sprites__(self):
        self.imageU = pygame.image.load(
            "bin/sprites/ghost1.gif").convert_alpha()
        self.imageD = pygame.image.load(
            "bin/sprites/ghost1.gif").convert_alpha()
        self.imageL = pygame.image.load(
            "bin/sprites/ghost1.gif").convert_alpha()
        self.imageR = pygame.image.load(
            "bin/sprites/ghost1.gif").convert_alpha()

        self.size = self.imageU.get_size()
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
        new_vector = (0, 0)
        if self.pressed_keys[self.UP]:
            new_vector = (0, -PACMAN_SPEED)
            self.imageC = self.imageU
        elif self.pressed_keys[self.DOWN]:
            new_vector = (0, PACMAN_SPEED)
            self.imageC = self.imageD
        elif self.pressed_keys[self.LEFT]:
            new_vector = (-PACMAN_SPEED, 0)
            self.imageC = self.imageL
        elif self.pressed_keys[self.RIGHT]:
            new_vector = (PACMAN_SPEED, 0)
            self.imageC = self.imageR
 
        new_rect = self.rect.move(new_vector[0], new_vector[1])
        
        # Check if rect is in moveable area
            # Yes -> update pos
            # No -> Don't update( and stop?)

        can_move = self.board.check_wall(new_rect)
        #self.board.check_pellet(new_rect)
        
        if can_move:
            #print(new_vector)
            self.rect.move_ip(new_vector[0], new_vector[1])

        # # Change position according to key_press
        # if self.pressed_keys[self.UP]:
        #     self.rect.move_ip(0, -PACMAN_SPEED)
        #     self.imageC = self.imageU
        # elif self.pressed_keys[self.DOWN]:
        #     self.rect.move_ip(0, PACMAN_SPEED)
        #     self.imageC = self.imageD
        # elif self.pressed_keys[self.LEFT]:
        #     self.rect.move_ip(-PACMAN_SPEED, 0)
        #     self.imageC = self.imageL
        # elif self.pressed_keys[self.RIGHT]:
        #     self.rect.move_ip(PACMAN_SPEED, 0)
        #     self.imageC = self.imageR

        # Ensure pacman stays in bounds.
        if new_rect.left < 0:
            new_rect.left = 0
        if new_rect.right > WIDTH:
            new_rect.right = WIDTH
        if new_rect.top <= 0:
            new_rect.top = 0
        if new_rect.bottom >= HEIGHT:
            new_rect.bottom = HEIGHT

        # self.rect = new_rect

        self.update_switch.unlock(self.finished_updating)


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