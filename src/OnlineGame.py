import socket
import time

import pygame

from classes import Ball, Paddle, Wall
from functions import checkCollision, checkPoints, checkWin, draw, isValidIp
from globals import BYTES_OF_DATA, COLORS, FPS, WINDOW_HEIGHT, WINDOW_WIDTH, font


def handleKeyPress(keys, player, side):
    if side == "server":
        if keys[pygame.K_w]:
            player.move("up")
        elif keys[pygame.K_s]:
            player.move("down")

    else:
        if keys[pygame.K_UP]:
            player.move("up")
        elif keys[pygame.K_DOWN]:
            player.move("down")


def printNames(WIN, playerLeftName, playerRightName):
    textHeight = font.size("sample text")[1]

    playerLeft = font.render(f"{playerLeftName}", True, COLORS["white"])
    WIN.blit(playerLeft, (80, 50 + 10 + textHeight))

    playerRight = font.render(f"{playerRightName}", True, COLORS["white"])
    textWidth = font.size(f"{playerRightName}")[0]
    WIN.blit(playerRight, (WINDOW_WIDTH - 80 - textWidth, 50 + 10 + textHeight))


class OnlineGame:
    def __init__(self, WIN, clock, side, playerIp, playerPort):
        self.WIN = WIN
        self.clock = clock
        self.side = side
        self.playerIp = playerIp
        self.playerPort = playerPort

        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.walls = Wall()
        self.playerLeft = Paddle("left")
        self.playerRight = Paddle("right")

        self.pointsLeft = 0
        self.pointsRight = 0

        self.mySocket = None
        self.myName = "localhost"

        # only for server
        self.connection = None

    def run(self):
        if not self.connectToGame():
            print("Couldn't connect to the game")
            return

        print("Connected to the game")

        if self.side == "server":
            self.runServerGame()
        else:
            self.runClientGame()

    def connectToGame(self):
        if self.side == "server":
            self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.myName = socket.gethostname()
            self.mySocket.bind((self.playerIp, int(self.playerPort)))
            self.mySocket.listen(1)

            self.connection, self.clientIP = self.mySocket.accept()
            return True

        elif self.side == "client":
            self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.myName = socket.gethostname()

            maxTries = 5
            retryInterval = 2

            for attempt in range(maxTries):
                try:
                    self.mySocket.connect((self.playerIp, int(self.playerPort)))
                    return True
                except:
                    print(
                        f"Attempt {attempt + 1}/{maxTries}: Connection refused. Retrying in {retryInterval} seconds..."
                    )
                    time.sleep(retryInterval)

            print(f"Failed to connect after {maxTries} attempts.")
            return False

        else:
            return False

    def runServerGame(self):
        clientName = self.connection.recv(BYTES_OF_DATA).decode()
        self.connection.send(self.myName.encode())

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.sendDataToClient(
                self.playerLeft.prevPosition,
                self.playerLeft.y,
                self.ball.x,
                self.ball.y,
            )
            (
                self.playerRight.prevPosition,
                self.playerRight.y,
            ) = self.readDataFromClient()

            self.playerLeft.prevPosition = self.playerLeft.y
            keys = pygame.key.get_pressed()
            handleKeyPress(keys, self.playerLeft, "server")
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
            printNames(self.WIN, self.myName, clientName)

            if checkWin(self.pointsLeft, self.pointsRight):
                break

            pygame.display.update()
            self.clock.tick(FPS)

    def runClientGame(self):
        self.mySocket.send(self.myName.encode())
        serverName = self.mySocket.recv(BYTES_OF_DATA).decode()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            (
                self.playerLeft.prevPosition,
                self.playerLeft.y,
                self.ball.x,
                self.ball.y,
            ) = self.readDataFromServer()
            self.sendDataToServer(self.playerRight.prevPosition, self.playerRight.y)

            self.playerRight.prevPosition = self.playerRight.y
            keys = pygame.key.get_pressed()
            handleKeyPress(keys, self.playerRight, "client")
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
            printNames(self.WIN, self.myName, serverName)

            if checkWin(self.pointsLeft, self.pointsRight):
                break

            pygame.display.update()
            self.clock.tick(FPS)

    # server -> client
    def sendDataToClient(self, prevPlayerY, playerY, ballX, ballY):
        self.connection.send(f"{prevPlayerY}/{playerY}/{ballX}/{ballY}".encode())

    # server <- client
    def readDataFromClient(self):
        data = self.connection.recv(BYTES_OF_DATA).decode().split("/")
        return float(data[0]), float(data[1])

    # client -> server
    def sendDataToServer(self, prevPlayerY, playerY):
        self.mySocket.send(f"{prevPlayerY}/{playerY}".encode())

    # client <- server
    def readDataFromServer(self):
        data = self.mySocket.recv(BYTES_OF_DATA).decode().split("/")
        return float(data[0]), float(data[1]), float(data[2]), float(data[3])


if __name__ == "__main__":
    data = input(
        "Enter ip address and port in format - ip:port like (255.255.255.255:2137)"
    )
    while not isValidIp(data):
        print("Incorrect ip and / or port!")
        data = input(
            "Enter ip address and port in format - ip:port like (255.255.255.255:2137)"
        )

    ip, port = data.split(":")

    side = input("Which side are you on (server / client)?: ")
    while side != "server" and side != "client":
        print("Incorrect side choice!")
        side = input("Which side are you on (server / client)?: ")

    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PONG")
    clock = pygame.time.Clock()

    onlineGame = OnlineGame(WIN, clock, side, ip, port)
    onlineGame.run()
