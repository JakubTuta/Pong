import socket
import time

from classess import Ball, Paddle, Wall
from globals import WINDOW_HEIGHT, WINDOW_WIDTH


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
            print("jesteś serwerem")
        else:
            print("jesteś klientem")

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
