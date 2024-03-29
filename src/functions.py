import re

from classes import Ball, Paddle, Wall
from globals import COLORS, POINTS_TO_WIN, WINDOW_WIDTH, font


def isValidIp(ip):
    pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}$"
    if re.match(pattern, ip) is not None:
        myIp, myPort = ip.split(":")
        for num in myIp.split("."):
            if not (0 <= int(num) <= 255):
                return False
        if not (1 <= int(myPort) <= 9999):
            return False
        return True
    return False


def setPaddles(playerLeft, playerRight):
    playerLeft.set_position()
    playerRight.set_position()


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
    ) and (
        isBetween(ball.y - Ball.radius, playerLeft.y, playerLeft.y + Paddle.height)
        or isBetween(ball.y + Ball.radius, playerLeft.y, playerLeft.y + Paddle.height)
    ):
        ball.calculateDirection(playerLeft)

    # ball with playerRight
    if isBetween(
        ball.x + Ball.radius,
        playerRight.x,
        playerRight.x + Paddle.width,
    ) and (
        isBetween(ball.y - Ball.radius, playerRight.y, playerRight.y + Paddle.height)
        or isBetween(ball.y + Ball.radius, playerRight.y, playerRight.y + Paddle.height)
    ):
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


def checkWin(pointsLeft, pointsRight):
    return pointsLeft == POINTS_TO_WIN or pointsRight == POINTS_TO_WIN
