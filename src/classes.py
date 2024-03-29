import pygame

from globals import COLORS, WINDOW_HEIGHT, WINDOW_WIDTH


class Ball:
    radius = 15
    baseSpeed = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedX = Ball.baseSpeed
        self.speedY = 0

    def draw(self, WIN):
        pygame.draw.circle(WIN, COLORS["white"], (self.x, self.y), Ball.radius)

    def move(self):
        self.x += self.speedX
        self.y += self.speedY

    def reset(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.speedY = 0

    def calculateDirection(self, paddle):
        self.speedX *= -1

        if paddle.prevPosition < paddle.currentPosition:
            if self.speedY < 0:
                self.speedY = 0
            self.speedY = Ball.baseSpeed

        elif paddle.prevPosition > paddle.currentPosition:
            if self.speedY > 0:
                self.speedY = 0
            self.speedY = -Ball.baseSpeed


class Wall:
    height = 30
    topY = height
    bottomY = WINDOW_HEIGHT - height

    def draw(self, WIN):
        pygame.draw.rect(WIN, COLORS["white"], (0, 0, WINDOW_WIDTH, Wall.height))
        pygame.draw.rect(
            WIN,
            COLORS["white"],
            (0, Wall.bottomY, WINDOW_WIDTH, Wall.height),
        )


class Paddle:
    height = 100
    width = 20
    speed = 10
    __padding = 50

    def __init__(self, side):
        if side == "left":
            self.x = Paddle.__padding
        else:
            self.x = WINDOW_WIDTH - Paddle.__padding - Paddle.width
        self.y = WINDOW_HEIGHT / 2 - Paddle.height / 2

        self.prevPosition = self.y
        self.currentPosition = self.y

    def draw(self, WIN):
        pygame.draw.rect(
            WIN, COLORS["white"], (self.x, self.y, Paddle.width, Paddle.height)
        )

    def move(self, direction):
        if direction == "up":
            if self.isMoveUpAvailable():
                self.y -= Paddle.speed

        elif direction == "down":
            if self.isMoveDownAvailable():
                self.y += Paddle.speed

        self.currentPosition = self.y

    def isMoveUpAvailable(self):
        return self.y > Wall.topY

    def isMoveDownAvailable(self):
        return self.y + Paddle.height < Wall.bottomY

    def set_position(self):
        self.prevPosition = self.y
