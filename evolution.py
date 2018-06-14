import tensorflow as tf
import copy
import time
import os
import pygame
import math
import random
import numpy as np

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0, 255, 0)
blue = (0, 0, 255)

WIDTH = 1000
HEIGHT = 1000
SIZE_QUOTIENT = 5
INIT_ORGANISMS_COUNT = 10
INIT_FOOD_COUNT = 10
FOOD_SIZE = 5


class Evolution(object):
    class Organism(object):
        def __init__(self):
            if random.randint(0,1) == 0:
                self.type = 'Carnivore'
            else:
                self.type = 'Herbivore'
            self.size = 1
            self.brain = list()
            self.x = random.randint(0,WIDTH-1)
            self.y = random.randint(0,HEIGHT-1)
    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Evolution')
        self.clock = pygame.time.Clock()

        self.organisms = [self.Organism() for i in range(INIT_ORGANISMS_COUNT)]
        self.food = [(random.randint(0, WIDTH-1),random.randint(0,HEIGHT-1)) for i in range(INIT_FOOD_COUNT)]

    def draw(self):
        for organism in self.organisms:
            if organism.type == 'Carnivore':
                pygame.draw.circle(self.gameDisplay, red, (organism.x, organism.y), organism.size*SIZE_QUOTIENT)
            else:
                pygame.draw.circle(self.gameDisplay, green, (organism.x, organism.y), organism.size*SIZE_QUOTIENT)
        for food in self.food:
            pygame.draw.line(self.gameDisplay, blue, (food[0] - FOOD_SIZE, food[1]), (food[0] + FOOD_SIZE, food[1]))
            pygame.draw.line(self.gameDisplay, blue, (food[0], food[1] - FOOD_SIZE), (food[0], food[1] + FOOD_SIZE))


    def start(self):
        self.end = False
        while not self.end:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    # if event.key == pygame.K_a:
                    #     self.player_move('left')
                    # if event.key == pygame.K_d:
                    #     self.player_move('right')
                    # if event.key == pygame.K_w:
                    #     self.player_move('up')
                    # if event.key == pygame.K_s:
                    #     self.player_move('down')
                    # if event.key == pygame.K_p:
                    #     pause = not pause
                    if event.key == pygame.K_r:
                        self.__init__()
                    if event.key == pygame.K_q:
                        self.end = True
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_LEFT:
                #         SUN_WEIGHT -= 100
                #         print(SUN_WEIGHT)
                #     if event.key == pygame.K_RIGHT:
                #         SUN_WEIGHT += 100
                #         print(SUN_WEIGHT)
                if event.type == pygame.QUIT:
                    self.end = True
                # if event.type == pygame.MOUSEBUTTONUP:
                #     pos = pygame.mouse.get_pos()
            self.gameDisplay.fill(white)
            self.draw()
            pygame.display.update()
            self.clock.tick(60)

a = Evolution()
a.start()