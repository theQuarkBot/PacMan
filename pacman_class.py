from distutils.dep_util import newer
import os, sys, random, pygame, threading
from settings import *
# from thread_safe_classes import Lightswitch
# from board import Board
import random

SPRITE_PATH = os.path.join(sys.path[0], "bin", "sprites")


class Pacman:
    def __init__(self, controls, update_switch, finished_updating, all_threads,
                 board, start_pos):
        # Initialize sprite image
        self.__init_sprites__()
        self.board = board
        self.start = start_pos
        self.reset()

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
        self.animU = []
        self.animD = []
        self.animL = []
        self.animR = []

        self.sprite_dim = (BLOCKSIZE, BLOCKSIZE)

        # Create sprite for each frame
        for i in range(1, 9):
            img_u = pygame.image.load(os.path.join(
                SPRITE_PATH, "pacman-u-" + str(i) + ".gif")).convert_alpha()
            img_d = pygame.image.load(os.path.join(
                SPRITE_PATH, "pacman-d-" + str(i) + ".gif")).convert_alpha()
            img_l = pygame.image.load(os.path.join(
                SPRITE_PATH, "pacman-l-" + str(i) + ".gif")).convert_alpha()
            img_r = pygame.image.load(os.path.join(
                SPRITE_PATH, "pacman-r-" + str(i) + ".gif")).convert_alpha()

            self.animU.append(pygame.transform.scale(img_u, self.sprite_dim))
            self.animD.append(pygame.transform.scale(img_d, self.sprite_dim))
            self.animL.append(pygame.transform.scale(img_l, self.sprite_dim))
            self.animR.append(pygame.transform.scale(img_r, self.sprite_dim))

        # Set starting animation
        self.anim_frame = 0
        self.animC = self.animR
        self.imageC = self.animC[self.anim_frame]

    def reset(self):
        # Reset sprite and position
        self.animC = self.animR
        self.animN = self.animC
        self.anim_frame = 0
        self.rect = self.animC[self.anim_frame].get_rect()
        self.rect.topleft = self.start

        # Initialize movement buffer
        self.cur_vector = pygame.Vector2((0, 0))
        self.next_vector = pygame.Vector2((0, 0))

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
        self.can_update.release()

    def __update_pos__(self):
        # Save the keypresses and next image for next velocity change
        if self.pressed_keys[self.UP]:
            self.next_vector.xy = 0, -PACMAN_SPEED
            self.animN = self.animU
        elif self.pressed_keys[self.DOWN]:
            self.next_vector.xy = 0, PACMAN_SPEED
            self.animN = self.animD
        elif self.pressed_keys[self.LEFT]:
            self.next_vector.xy = -PACMAN_SPEED, 0
            self.animN = self.animL
        elif self.pressed_keys[self.RIGHT]:
            self.next_vector.xy = PACMAN_SPEED, 0
            self.animN = self.animR

        # Determine whether it can go in the new direction
        new_rect = self.rect.move(self.next_vector.x, self.next_vector.y)
        self.__try_teleport_through_tunnel__(new_rect)
        can_move = self.board.check_wall(new_rect)

        # Update the current move if the new move is possible
        if can_move:
            self.cur_vector.xy = self.next_vector.xy
            self.animC = self.animN
        # Otherwise try moving in the old direction
        else:
            new_rect = self.rect.move(self.cur_vector.x, self.cur_vector.y)
            self.__try_teleport_through_tunnel__(new_rect)
            can_move = self.board.check_wall(new_rect)

        # Update position
        if can_move:
            self.board.check_pellet(new_rect)
            self.rect.topleft = new_rect.topleft
            self.imageC = self.animC[self.anim_frame]
            self.anim_frame = (self.anim_frame + 1) % 8

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


class Ghost:
    def __init__(self, controls, update_switch, finished_updating, all_threads,
                 board, start_pos):
        # Initialize sprite image
        self.__init_sprites__()
        self.board = board
        self.start = start_pos
        self.reset()

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
        self.anim = []

        self.sprite_dim = (BLOCKSIZE, BLOCKSIZE)

        for i in range(1, 7):
            img = pygame.image.load(os.path.join(
                SPRITE_PATH, "ghost-" + str(i) + ".gif")).convert_alpha()

            self.anim.append(pygame.transform.scale(img, self.sprite_dim))

        self.anim_frame = 0
        self.imageC = self.anim[self.anim_frame]

    def reset(self):
        self.rect = self.imageC.get_rect()
        self.rect.topleft = self.start

        # Initialize movement buffer
        self.cur_vector = pygame.Vector2((0, 0))
        self.next_vector = pygame.Vector2((0, 0))

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
        self.can_update.release()

    def __update_pos__(self):
        # Save the keypresses and next image for next velocity change
        if self.pressed_keys[self.UP]:
            self.next_vector.xy = 0, -PACMAN_SPEED
        elif self.pressed_keys[self.DOWN]:
            self.next_vector.xy = 0, PACMAN_SPEED
        elif self.pressed_keys[self.LEFT]:
            self.next_vector.xy = -PACMAN_SPEED, 0
        elif self.pressed_keys[self.RIGHT]:
            self.next_vector.xy = PACMAN_SPEED, 0

        # Determine whether it can go in the new direction
        new_rect = self.rect.move(self.next_vector.x, self.next_vector.y)
        self.__try_teleport_through_tunnel__(new_rect)
        can_move = self.board.check_wall(new_rect)

        # Update the current move if the new move is possible
        if can_move:
            self.cur_vector.xy = self.next_vector.xy
        # Otherwise try moving in the old direction
        else:
            new_rect = self.rect.move(self.cur_vector.x, self.cur_vector.y)
            self.__try_teleport_through_tunnel__(new_rect)
            can_move = self.board.check_wall(new_rect)

        # Update position
        if can_move:
            self.rect.topleft = new_rect.topleft
            self.imageC = self.anim[self.anim_frame]
            self.anim_frame = (self.anim_frame + 1) % 6

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


class RandomGhost:
    def __init__(self, update_switch, finished_updating, all_threads,
                 board, start_pos):
        # Initialize sprite image
        self.__init_sprites__()
        self.board = board
        self.start = start_pos
        self.reset()

        # Update synchronization variables
        self.can_update = threading.Semaphore(0)
        self.update_switch = update_switch
        self.finished_updating = finished_updating
        self.mutex = threading.Semaphore(1)

        self.running = True

        #self.pot_move = 0
        #self.pot_vector = pygame.Vector2((0, 0))

        # Used to give time between wall collision and next move
        #self.hit_wall_time = 0
        # Used to make sure that we don't try to crash back into the wall
        # immediately after moving away
        self.hit_wall = False

        # Start movement thread
        self.thread = threading.Thread(target=self.__run__)
        all_threads.append(self.thread)
        self.thread.start()

    def __init_sprites__(self):
        self.anim = []

        self.sprite_dim = (BLOCKSIZE, BLOCKSIZE)

        for i in range(1, 7):
            img = pygame.image.load(os.path.join(
                SPRITE_PATH, "ghost-" + str(i) + ".gif")).convert_alpha()

            self.anim.append(pygame.transform.scale(img, self.sprite_dim))

        self.anim_frame = 0
        self.imageC = self.anim[self.anim_frame]

    def reset(self):
        self.rect = self.imageC.get_rect()
        self.rect.topleft = self.start

        # Initialize movement buffer
        self.cur_vector = pygame.Vector2((0, 0))
        self.next_vector = pygame.Vector2((0, 0))

        self.next_move = 0
        self.time = 0

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
        self.can_update.release()

    def __update_pos__(self):
        # Save the keypresses and next image for next velocity change

        if self.time == 100:
            self.next_move = random.randint(0, 3)
            self.time = 0
        self.time += 1

        # Used to determine values for potential turning
        #if self.pot_move == 0:
        #    self.pot_vector.xy = 0, -PACMAN_SPEED
        #elif self.pot_move == 1:
        #    self.pot_vector.xy = 0, PACMAN_SPEED
        #elif self.pot_move == 2:
        #    self.pot_vector.xy = -PACMAN_SPEED, 0
        #elif self.pot_move == 3:
        #    self.pot_vector.xy = PACMAN_SPEED, 0

        if self.next_move == 0:
            self.next_vector.xy = 0, -PACMAN_SPEED
        elif self.next_move == 1:
            self.next_vector.xy = 0, PACMAN_SPEED
        elif self.next_move == 2:
            self.next_vector.xy = -PACMAN_SPEED, 0
        elif self.next_move == 3:
            self.next_vector.xy = PACMAN_SPEED, 0

        # Determine whether it can go in the new direction
        new_rect = self.rect.move(self.next_vector.x, self.next_vector.y)
        self.__try_teleport_through_tunnel__(new_rect)
        can_move = self.board.check_wall_rand_ghost(new_rect, self.next_move)

        # Used to see if a potential new direction is possible
        # without having to wait for a collision with a wall
        #pot_rect = self.rect.move(self.pot_vector.x, self.pot_vector.y)
        #self.__try_teleport_through_tunnel_pot__(pot_rect)
        #can_moveP = self.board.check_wall_rand_ghost(pot_rect)

        # Want to use the new move if possible
        #if can_moveP:
        #    self.cur_vector.xy = self.pot_vector.xy
        # Update the current move if the new move is possible
        if can_move:
            self.cur_vector.xy = self.next_vector.xy
        # Otherwise try moving in the old direction
        else:
            new_rect = self.rect.move(self.cur_vector.x, self.cur_vector.y)
            self.__try_teleport_through_tunnel__(new_rect)
            can_move = self.board.check_wall_rand_ghost(
                new_rect, self.next_move)

        # only changes value when contact with wall
        if not can_move:
            old = get_rev(self.next_move)
            self.next_move = random.randint(0, 3)
            while self.next_move == old:
                self.next_move = random.randint(0, 3)

        # Update position
        #if can_moveP:
        #    self.rect.topleft = pot_rect.topleft
        if can_move:
            self.rect.topleft = new_rect.topleft
            self.imageC = self.anim[self.anim_frame]
            self.anim_frame = (self.anim_frame + 1) % 6

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

    def __try_teleport_through_tunnel_pot__(self, rect):
        if rect.left < 0:
            rect.right = WIDTH - 2
        if rect.right >= WIDTH:
            rect.left = 0
        if rect.top <= 0:
            rect.bottom = HEIGHT - 2
        if rect.bottom >= HEIGHT:
            rect.top = 0


def get_rev(i):
    #return the opposite of the given direction
    if i == 0:
        return 1
    elif i == 1:
        return 0
    elif i == 2:
        return 3
    else:
        return 2
