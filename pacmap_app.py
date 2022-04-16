import pygame
import sys
import random
from settings import *

pygame.init()
vec = pygame.math.Vector2

class game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        
        

        # self.walls = []
        # self.coins = []
        # self.enemies = []
        # self.players = []
        # self.players.append(Player())

        self.state = START_STATE

    def run(self):
        while self.running:
            if self.state == START_STATE:
                self.start_events()


        