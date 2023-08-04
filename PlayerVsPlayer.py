import pygame

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 600
FPS = 60

COLORS = {"black": (0, 0, 0), "white": (255, 255, 255)}

pygame.init()
font = pygame.font.SysFont(None, 60)


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
            self.speedY = Ball.baseSpeed

        elif paddle.prevPosition > paddle.currentPosition:
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
    __padding = 50
    __speed = 10

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
                self.y -= Paddle.__speed

        elif direction == "down":
            if self.isMoveDownAvailable():
                self.y += Paddle.__speed

        self.currentPosition = self.y

    def isMoveUpAvailable(self):
        return self.y > Wall.topY

    def isMoveDownAvailable(self):
        return self.y + Paddle.height < Wall.bottomY

    def set(self):
        self.prevPosition = self.y


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


def main():
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PONG")
    clock = pygame.time.Clock()

    ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    walls = Wall()
    playerLeft = Paddle("left")
    playerRight = Paddle("right")

    pointsLeft = 0
    pointsRight = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        everyFrame(playerLeft, playerRight)
        keys = pygame.key.get_pressed()
        handleKeyPress(keys, playerLeft, playerRight)
        move(ball)
        checkCollision(ball, playerLeft, playerRight)
        pointsLeft, pointsRight = checkPoints(ball, pointsLeft, pointsRight)
        draw(WIN, ball, walls, playerLeft, playerRight, pointsLeft, pointsRight)

        pygame.display.update()
        clock.tick(FPS)
