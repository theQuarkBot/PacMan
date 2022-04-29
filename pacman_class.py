from distutils.dep_util import newer
import os, sys, random, pygame, threading
from settings import *
from abc import ABC, abstractmethod
import random

SPRITE_PATH = os.path.join(sys.path[0], "bin", "sprites")

class Character(ABC):
    def __init__(self, update_switch, finished_updating, all_threads,
                 board, start_pos, controls=None, color=GHOST_RED):
        self.color = color
        self.board = board
        self.start = start_pos
        self.reset()

        # Set controls
        if not controls == None:
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

    @abstractmethod
    def __init_sprites__(self):
        pass

    @abstractmethod
    def reset(self):
        pass


    def update_event(self, pressed_keys):
        self.update_switch.lock(self.finished_updating)

        self.pressed_keys = pressed_keys

        self.can_update.release()

    @abstractmethod
    def __update_pos__(self):
        pass

    def __run__(self):
        while self.running:
            self.can_update.acquire()
            self.__update_pos__()

    def stop(self):
        self.running = False
        self.can_update.release()

    def __try_teleport_through_tunnel__(self, rect):
        if rect.left < 0:
            rect.right = WIDTH - 2
        if rect.right >= WIDTH:
            rect.left = 0
        if rect.top <= 0:
            rect.bottom = HEIGHT - 2
        if rect.bottom >= HEIGHT:
            rect.top = 0

class Pacman(Character):

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
        self.__init_sprites__()
        self.animC = self.animR
        self.animN = self.animC
        self.anim_frame = 0
        self.rect = self.animC[self.anim_frame].get_rect()
        self.rect.topleft = self.start

        # Initialize movement buffer
        self.cur_vector = pygame.Vector2((0, 0))
        self.next_vector = pygame.Vector2((0, 0))

        self.speed = PACMAN_SPEED

    def __update_pos__(self):
        # Save the keypresses and next image for next velocity change
        if self.pressed_keys[self.UP]:
            self.next_vector.xy = 0, -self.speed
            self.animN = self.animU
        elif self.pressed_keys[self.DOWN]:
            self.next_vector.xy = 0, self.speed
            self.animN = self.animD
        elif self.pressed_keys[self.LEFT]:
            self.next_vector.xy = -self.speed, 0
            self.animN = self.animL
        elif self.pressed_keys[self.RIGHT]:
            self.next_vector.xy = self.speed, 0
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

class Ghost(Character):

    def __init_sprites__(self):
        self.anim = []

        self.sprite_dim = (BLOCKSIZE, BLOCKSIZE)

        for i in range(1, 7):
            img = pygame.image.load(os.path.join(
                SPRITE_PATH, "ghost-" + str(i) + ".gif")).convert_alpha()

            # Change ghost color if necessary
            for y in range(0, 16):
                for x in range(0, 16):
                    # default, red ghost body color
                    if img.get_at((x, y)) == GHOST_RED:
                        if self.weak:
                            img.set_at((x, y), GHOST_WEAK)
                        elif img.get_at((x, y)) == GHOST_RED:
                            img.set_at((x, y), self.color)

            self.anim.append(pygame.transform.scale(img, self.sprite_dim))

        self.anim_frame = 0
        self.imageC = self.anim[self.anim_frame]

    def reset(self):
        self.weak = False
        self.weak_time = 0
        self.speed = GHOST_SPEED

        self.__init_sprites__()

        self.rect = self.imageC.get_rect()
        self.rect.topleft = self.start

        # Initialize movement buffer
        self.cur_vector = pygame.Vector2((0, 0))
        self.next_vector = pygame.Vector2((0, 0))

        self.next_move = 0
        self.time = 0

    def __run__(self):
        while self.running:
            self.can_update.acquire()
            self.__update_weakness__()
            self.__update_pos__()


    def is_weak(self):
        return self.weak

    def set_weak(self):
        self.weak = True
        self.weak_time = 0

    def __update_weakness__(self):
        if self.weak:
            self.weak_time += 1
            if self.weak_time == 1:
                self.__init_sprites__()
                self.speed = GHOST_WEAK_SPEED
            elif self.weak_time == 360:
                self.weak = False
                self.__init_sprites__()

                if self.rect.top % 2 == 1:
                    self.rect.top -= 1
                if self.rect.left % 2 == 1:
                    self.rect.left -= 1

                # Reset speed
                self.speed = GHOST_SPEED
        
    def __update_pos__(self):
        # Save the keypresses and next image for next velocity change
        if self.pressed_keys[self.UP]:
            self.next_vector.xy = 0, -self.speed
        elif self.pressed_keys[self.DOWN]:
            self.next_vector.xy = 0, self.speed
        elif self.pressed_keys[self.LEFT]:
            self.next_vector.xy = -self.speed, 0
        elif self.pressed_keys[self.RIGHT]:
            self.next_vector.xy = self.speed, 0

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

class RandomGhost(Ghost):
    def __update_pos__(self):
        if self.time == 100:
            self.next_move = random.randint(0, 3)
            self.time = 0
        self.time += 1

        if self.next_move == 0:
            self.next_vector.xy = 0, -self.speed
        elif self.next_move == 1:
            self.next_vector.xy = 0, self.speed
        elif self.next_move == 2:
            self.next_vector.xy = -self.speed, 0
        elif self.next_move == 3:
            self.next_vector.xy = self.speed, 0

        # Determine whether it can go in the new direction
        new_rect = self.rect.move(self.next_vector.x, self.next_vector.y)
        self.__try_teleport_through_tunnel__(new_rect)
        can_move = self.board.check_wall_rand_ghost(new_rect, self.next_move)

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
        
    
