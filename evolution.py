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
INIT_ORGANISMS_COUNT = 30
INIT_FOOD_COUNT = 30
FOOD_SIZE = 5
TYPE_RATIO = 0.5
NUM_EVOLUTIONS = 1

MINIMUM_ORGANISMS = 1

TICK_TIME = 0.1
COMBAT_RANGE = 10

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

class Organism(object):
    def __init__(self):
        self.size = 1
        self.brain = list()
        self.x = random.randint(0,WIDTH-1)
        self.y = random.randint(0,HEIGHT-1)
        self.genotype = Genotype(self)
        self.age = 0
    def move(self, organisms, food):
        self.age += 1
        moves = [0, 0, 0, 0] #[Left, Right, Top, Bottom]
        moves[0] = self.evaluate(organisms, food, self.x - 1, self.y    )  
        moves[1] = self.evaluate(organisms, food, self.x + 1, self.y    )
        moves[2] = self.evaluate(organisms, food, self.x    , self.y - 1)
        moves[3] = self.evaluate(organisms, food, self.x    , self.y + 1)
        print(moves)
        best = np.argmax(moves)
        if best == 0:
            self.x -= 5
        elif best == 1:
            self.x += 5
        elif best == 2:
            self.y -= 5
        elif best == 3:
            self.y += 5
        
    def evaluate(self, organisms, food, x, y):
        overall_mate = 0
        overall_fear = 0
        overall_hunger = 0
        overall_kill = 0
        for organism in organisms:
            if self is organism:
                continue
            distance = euclidean_distance(x, y, organism.x, organism.y) / (math.sqrt(WIDTH**2+HEIGHT**2))
            mate = 0
            fear = 0
            kill = 0
            if type(self) == type(organism):
                mate += self.genotype.mate * distance * (-1)
            else:
                mate = 0

            fear = self.genotype.flee * distance * (-1)
            kill = self.genotype.kill * distance * (-1)

            overall_mate += mate
            overall_fear += fear
            overall_kill += kill
        for piece in food:
            distance = euclidean_distance(piece[0], piece[1], x, y) / (math.sqrt(WIDTH**2+HEIGHT**2))
            hunger = self.genotype.food_lust * distance * (-1)
            overall_hunger += hunger
        return overall_fear + overall_hunger + overall_kill + overall_mate
class Carnivore(Organism):
    def __init__(self):
        super(Carnivore, self).__init__()
class Herbivore(Organism):
    def __init__(self):
        super(Herbivore, self).__init__()

class Genotype(object):
    def __init__(self, host):
        self.host = type(host)
        self.mate = random.randint(0,10)
        self.food_lust = random.randint(0,10)
        self.kill = random.randint(0,10)
        self.flee = random.randint(0,10)
        if self.host == Carnivore:
            self.kill *= 2
            self.flee = 0
        else:
            self.flee *= 2
            self.kill = 0



class Evolution(object):

    def __init__(self):
        pygame.init()
        self.time = time.time()
        self.gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Evolution')
        self.clock = pygame.time.Clock()
        self.num_generations = NUM_EVOLUTIONS

        self.organisms = [Carnivore() if random.random() > TYPE_RATIO else Herbivore() for i in range(INIT_ORGANISMS_COUNT)]
        self.food = [(random.randint(0, WIDTH-1),random.randint(0,HEIGHT-1)) for i in range(INIT_FOOD_COUNT)]

    def move(self):
        actual_time = time.time() 
        if actual_time - self.time > TICK_TIME:
            self.time = actual_time
            for organism in self.organisms:
                organism.move(self.organisms, self.food)
        dead = []
        for i1, organism1 in enumerate(self.organisms):
            for i2, organism2 in enumerate(self.organisms):
                if organism1 is organism2:
                    continue
                if euclidean_distance(organism1.x, organism1.y, organism2.x, organism2.y) < COMBAT_RANGE:
                    if type(organism1) == Carnivore:
                        if type(organism2) == Herbivore:
                            dead.append(i2)
                        if type(organism2) == Carnivore:
                            if random.randint(0,1) == 0:
                                dead.append(i1)
                            else:
                                dead.append(i2)
                    if type(organism1) == Herbivore:
                        if type(organism2) == Herbivore:
                            pass
                        if type(organism2) == Carnivore:
                            dead.append(i1)
        for i in dead:
            try:
                # pass
                del self.organisms[i]
            except IndexError:
                pass
        eaten_food = []
        for i, organism in enumerate(self.organisms):
            for u, food in enumerate(self.food):
                if euclidean_distance(organism.x, organism.y, food[0], food[1]) < COMBAT_RANGE:
                    eaten_food.append(u)
        for i in eaten_food:
            del self.food[i]

    def draw(self):
        for organism in self.organisms:
            if type(organism) == Carnivore:
                pygame.draw.circle(self.gameDisplay, red, (organism.x, organism.y), organism.size*SIZE_QUOTIENT)
            else:
                pygame.draw.circle(self.gameDisplay, green, (organism.x, organism.y), organism.size*SIZE_QUOTIENT)
        for food in self.food:
            pygame.draw.line(self.gameDisplay, blue, (food[0] - FOOD_SIZE, food[1]), (food[0] + FOOD_SIZE, food[1]))
            pygame.draw.line(self.gameDisplay, blue, (food[0], food[1] - FOOD_SIZE), (food[0], food[1] + FOOD_SIZE))

    def epoch_ended(self):
        if len(self.organisms) < MINIMUM_ORGANISMS:
            return True
    def cross_population(self):
        order = sorted(self.organisms, key=lambda x: x.age, reverse=True)
    def evolve(self):
        for generation in range(self.num_generations):
            self.start()
            self.cross_population()
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
            if self.epoch_ended():
                self.end = True
                return
            self.gameDisplay.fill(white)
            self.move()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)

a = Evolution()
a.evolve()
