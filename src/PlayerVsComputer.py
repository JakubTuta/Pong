import numpy as np
import pygame
import skfuzzy as fuzz
from skfuzzy import control

from classes import Ball, Paddle, Wall
from functions import checkCollision, checkPoints, checkWin, draw, setPaddles
from globals import FPS, WINDOW_HEIGHT, WINDOW_WIDTH


def handleKeyPress(player):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.move("up")
    elif keys[pygame.K_s]:
        player.move("down")


class PVEGame:
    def __init__(self, WIN, clock):
        self.WIN = WIN
        self.clock = clock
        self.walls = Wall()
        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.playerLeft = Paddle("left")
        self.playerBot = Paddle("right")

        self.__setup_fuzzy()

    def __setup_fuzzy(self):
        distance = control.Antecedent(
            universe=np.arange(-WINDOW_HEIGHT, WINDOW_HEIGHT + 1),
            label="distance",
        )
        movement = control.Consequent(
            universe=np.arange(-Paddle.speed, Paddle.speed + 1),
            label="movement",
        )

        distance["above"] = fuzz.trimf(
            distance.universe, [-WINDOW_HEIGHT, -WINDOW_HEIGHT, 0]
        )
        distance["center"] = fuzz.trimf(
            distance.universe, [-WINDOW_HEIGHT, 0, WINDOW_HEIGHT]
        )
        distance["below"] = fuzz.trimf(
            distance.universe, [0, WINDOW_HEIGHT, WINDOW_HEIGHT]
        )

        movement["up"] = fuzz.trimf(
            movement.universe, [-Paddle.speed, -Paddle.speed, 0]
        )
        movement["stay"] = fuzz.trimf(
            movement.universe, [-Paddle.speed, 0, Paddle.speed]
        )
        movement["down"] = fuzz.trimf(
            movement.universe, [0, Paddle.speed, Paddle.speed]
        )

        rule_above = control.Rule(
            distance["above"],
            movement["up"],
        )
        rule_center = control.Rule(
            distance["center"],
            movement["stay"],
        )
        rule_below = control.Rule(
            distance["below"],
            movement["down"],
        )
        control_system = control.ControlSystem(
            [
                rule_above,
                rule_center,
                rule_below,
            ]
        )
        self.controller = control.ControlSystemSimulation(control_system)

    def run(self):
        pointsLeft = 0
        pointsRight = 0

        gameRunning = True

        while gameRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            setPaddles(self.playerLeft, self.playerBot)

            self.__botAction()
            handleKeyPress(self.playerLeft)
            self.ball.move()
            checkCollision(self.ball, self.playerLeft, self.playerBot)
            pointsLeft, pointsRight = checkPoints(self.ball, pointsLeft, pointsRight)
            draw(
                self.WIN,
                self.ball,
                self.walls,
                self.playerLeft,
                self.playerBot,
                pointsLeft,
                pointsRight,
            )

            if checkWin(pointsLeft, pointsRight):
                gameRunning = False

            pygame.display.update()
            self.clock.tick(FPS)

    def __botAction(self):
        self.controller.input["distance"] = self.ball.y - (
            self.playerBot.y + Paddle.height / 2
        )
        self.controller.compute()
        paddle_speed = self.controller.output["movement"] * 25

        if (
            self.playerBot.y > self.walls.topY
            and self.playerBot.y + Paddle.height < self.walls.bottomY
        ):
            self.playerBot.y += paddle_speed


if __name__ == "__main__":
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PONG")
    clock = pygame.time.Clock()

    pveGame = PVEGame(WIN, clock)
    pveGame.run()
