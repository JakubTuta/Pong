import pygame

from classess import Ball, Paddle, Wall
from globals import COLORS, FPS, WINDOW_HEIGHT, WINDOW_WIDTH, font


def everyFrame(playerLeft, playerRight):
    playerLeft.set()
    playerRight.set()


def handleKeyPress(keys, playerLeft, playerRight):
    if keys[pygame.K_w]:
        playerLeft.move("up")
    elif keys[pygame.K_s]:
        playerLeft.move("down")

    if keys[pygame.K_UP]:
        playerRight.move("up")
    elif keys[pygame.K_DOWN]:
        playerRight.move("down")


def move(ball):
    ball.move()


def isBetween(object, bottomRange, topRange):
    return object <= topRange and object >= bottomRange


def checkCollision(ball, playerLeft, playerRight):
    # ball with walls
    if ball.y - Ball.radius <= Wall.topY or ball.y + Ball.radius >= Wall.bottomY:
        ball.speedY *= -1

    # ball with playerLeft
    if isBetween(
        ball.x - Ball.radius,
        playerLeft.x,
        playerLeft.x + Paddle.width,
    ) and isBetween(ball.y, playerLeft.y, playerLeft.y + Paddle.height):
        ball.calculateDirection(playerLeft)

    # ball with playerRight
    if isBetween(
        ball.x + Ball.radius,
        playerRight.x,
        playerRight.x + Paddle.width,
    ) and isBetween(ball.y, playerRight.y, playerRight.y + Paddle.height):
        ball.calculateDirection(playerRight)


def checkPoints(ball, pointsLeft, pointsRight):
    if ball.x + Ball.radius < 0:
        pointsRight += 1
        ball.reset()

    elif ball.x - Ball.radius > WINDOW_WIDTH:
        pointsLeft += 1
        ball.reset()

    return pointsLeft, pointsRight


def draw(WIN, ball, walls, playerLeft, playerRight, pointsLeft, pointsRight):
    WIN.fill((COLORS["black"]))

    ball.draw(WIN)
    walls.draw(WIN)
    playerLeft.draw(WIN)
    playerRight.draw(WIN)

    pointsLeftText = font.render(f"{pointsLeft}", True, COLORS["white"])
    WIN.blit(pointsLeftText, (80, 50))

    pointsRightText = font.render(f"{pointsRight}", True, COLORS["white"])
    textWidth = font.size(f"{pointsRight}")[0]
    WIN.blit(pointsRightText, (WINDOW_WIDTH - 80 - textWidth, 50))


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

            everyFrame(self.playerLeft, self.playerRight)
            keys = pygame.key.get_pressed()
            handleKeyPress(keys, self.playerLeft, self.playerRight)
            move(self.ball)
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

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PONG")
    clock = pygame.time.Clock()

    pvpGame = PVPGame(WIN, clock)
    pvpGame.run()
