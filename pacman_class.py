#!/usr/bin/python3

import os, sys, random
import pygame
# from pygame.locals import (
#     RLEACCEL,
#     K_UP,
#     K_DOWN,
#     K_LEFT,
#     K_RIGHT,
#     K_ESCAPE,
#     KEYDOWN,
#     QUIT,
#     K_w,
#     K_a,
#     K_s,
#     K_d,
# )
from thread_safe_classes import *
from settings import *
vec = pygame.math.Vector2


class Player:
    def __init__(self, controls, update_switch, finished_updating, all_threads):
        # Initialize sprite image
        self.__init_sprites__()
        self.imageC = self.imageR
        self.rect = self.imageC.get_rect()

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
            "bin/large_sprites/pac_up.png").convert()
        self.imageD = pygame.image.load(
            "bin/large_sprites/pac_down.png").convert()
        self.imageL = pygame.image.load(
            "bin/large_sprites/pac_left.png").convert()
        self.imageR = pygame.image.load(
            "bin/large_sprites/pac_right.png").convert()

        self.size = self.imageU.get_size()
        self.__sprite_dimensions__ = (int(self.size[0]/3), int(self.size[1]/3))
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
        if self.pressed_keys[self.UP]:
            self.rect.move_ip(0, -PACMAN_SPEED)
            self.imageC = self.imageU
        elif self.pressed_keys[self.DOWN]:
            self.rect.move_ip(0, PACMAN_SPEED)
            self.imageC = self.imageD
        elif self.pressed_keys[self.LEFT]:
            self.rect.move_ip(-PACMAN_SPEED, 0)
            self.imageC = self.imageL
        elif self.pressed_keys[self.RIGHT]:
            self.rect.move_ip(PACMAN_SPEED, 0)
            self.imageC = self.imageR

        # Ensure pacman stays in bounds.
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

        self.update_switch.unlock(self.finished_updating)

def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    player_update_switch = Lightswitch()
    finished_updating = threading.Semaphore(1)

    threads = []
    players = []

    player1 = Player(ARROW_CONTROLS, player_update_switch, finished_updating, threads)
    players.append(player1)

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
        screen.blit(player1.imageC, player1.rect)

        pygame.display.flip()

        pressed_keys = pygame.key.get_pressed()
        player1.update_event(pressed_keys)

        clock.tick(FPS)
    pygame.quit()

    for thread in threads:
        thread.join()

    print("Thank you for playing!")

if __name__ == "__main__":
    main()