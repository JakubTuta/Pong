import pygame

from classes import Ball, Paddle, Wall
from functions import checkCollision, checkPoints, checkWin, draw, setPaddles
from globals import FPS, WINDOW_HEIGHT, WINDOW_WIDTH


def handleKeyPress(keys, playerLeft, playerRight):
    if keys[pygame.K_w]:
        playerLeft.move("up")
    elif keys[pygame.K_s]:
        playerLeft.move("down")

    if keys[pygame.K_UP]:
        playerRight.move("up")
    elif keys[pygame.K_DOWN]:
        playerRight.move("down")


class PVPGame:
    def __init__(self, WIN, clock):
        self.WIN = WIN
        self.clock = clock

        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.walls = Wall()
        self.playerLeft = Paddle("left")
        self.playerRight = Paddle("right")

        self.pointsLeft = 0
        self.pointsRight = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            setPaddles(self.playerLeft, self.playerRight)
            keys = pygame.key.get_pressed()
            handleKeyPress(keys, self.playerLeft, self.playerRight)
            self.ball.move()
            checkCollision(self.ball, self.playerLeft, self.playerRight)
            self.pointsLeft, self.pointsRight = checkPoints(
                self.ball, self.pointsLeft, self.pointsRight
            )
            draw(
                self.WIN,
                self.ball,
                self.walls,
                self.playerLeft,
                self.playerRight,
                self.pointsLeft,
                self.pointsRight,
            )

            if checkWin(self.pointsLeft, self.pointsRight):
                break

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PONG")
    clock = pygame.time.Clock()

    pvpGame = PVPGame(WIN, clock)
    pvpGame.run()
