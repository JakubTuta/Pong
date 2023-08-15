import os
import pickle

import neat
import pygame

from classess import Ball, Paddle, Wall
from functions import checkCollision, checkPoints, checkWin, draw, setPaddles
from globals import FPS, WINDOW_HEIGHT, WINDOW_WIDTH

LOAD_BEST_POPULATION = True
SAVE_BEST_POPULATION = True


def handleKeyPress(keys, playerLeft):
    if keys[pygame.K_w]:
        playerLeft.move("up")
    elif keys[pygame.K_s]:
        playerLeft.move("down")


def botMove(direction, paddle):
    if direction == "up":
        paddle.move("up")
    elif direction == "down":
        paddle.move("down")


class PVEGame:
    def __init__(self, WIN, clock):
        self.WIN = WIN
        self.clock = clock

        self.walls = Wall()

        local_dir = os.path.dirname(__file__)
        self.config_path = os.path.join(local_dir, "NEAT_config.txt")

    def run(self):
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            self.config_path,
        )

        population = neat.Population(config)

        if LOAD_BEST_POPULATION:
            population = PVEGame.loadPopulation("population.dat")

        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)

        population.run(self.mainGame, 1)

        if SAVE_BEST_POPULATION:
            PVEGame.savePopulation("population.dat", population)

    def mainGame(self, genomes, config):
        nets = []
        ge = []
        paddles = []

        for _, g in genomes:
            g.fitness = 0
            nets.append(neat.nn.FeedForwardNetwork.create(g, config))
            ge.append(g)
            paddles.append(Paddle("right"))

        for i, paddle in enumerate(paddles):
            self.playerLeft = Paddle("left")
            ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

            pointsLeft = 0
            pointsRight = 0

            gameRunning = True

            while gameRunning:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                ge[i].fitness = pointsRight - pointsLeft
                newDirection = PVEGame.handleNEAT(nets[i], paddle, ball)
                botMove(newDirection, paddle)

                setPaddles(self.playerLeft, paddle)
                keys = pygame.key.get_pressed()
                handleKeyPress(keys, self.playerLeft)
                ball.move()
                checkCollision(ball, self.playerLeft, paddle)
                pointsLeft, pointsRight = checkPoints(ball, pointsLeft, pointsRight)
                draw(
                    self.WIN,
                    ball,
                    self.walls,
                    self.playerLeft,
                    paddle,
                    pointsLeft,
                    pointsRight,
                )

                if checkWin(pointsLeft, pointsRight):
                    gameRunning = False

                pygame.display.update()
                self.clock.tick(2 * FPS)

    @staticmethod
    def savePopulation(filename, population):
        with open(filename, "wb") as file:
            pickle.dump(population, file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def loadPopulation(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)

    @staticmethod
    def handleNEAT(net, paddle, ball):
        inputs = [paddle.y, paddle.y + Paddle.height, ball.x, ball.y]

        output = net.activate((inputs))
        outputList = [("stay", output[0]), ("up", output[1]), ("down", output[2])]
        outputList.sort(key=lambda x: x[1], reverse=True)

        return outputList[0][0]


if __name__ == "__main__":
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PONG")
    clock = pygame.time.Clock()

    pveGame = PVEGame(WIN, clock)
    pveGame.run()
