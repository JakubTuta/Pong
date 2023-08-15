import tkinter

import pygame

from functions import isValidIp
from globals import *
from OnlineGame import OnlineGame
from PlayerVsComputer import PVEGame
from PlayerVsPlayer import PVPGame


def playGame(window, side, gameMode, inputIp):
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PONG")
    clock = pygame.time.Clock()

    if gameMode == "pvp":
        window.destroy()
        pvpGame = PVPGame(WIN, clock)
        pvpGame.run()

    elif gameMode == "pve":
        window.destroy()
        pveGame = PVEGame(WIN, clock)
        pveGame.run()

    elif gameMode == "online":
        if not isValidIp(inputIp):
            print("Incorrect ip and/or port")
            pygame.quit()
            return

        window.destroy()
        playerIp, playerPort = inputIp.split(":")
        onlineGame = OnlineGame(WIN, clock, side, playerIp, playerPort)
        onlineGame.run()

    else:
        return


def main():
    window = tkinter.Tk()
    window.title("PONG")
    window.resizable(False, False)

    gameMode = tkinter.StringVar(value="pvp")
    tkinter.Radiobutton(
        window,
        text="Play against another Player",
        variable=gameMode,
        value="pvp",
        font=("Times New Roman", 15),
    ).grid(row=0, column=0, padx=15, pady=15, sticky=tkinter.W)

    tkinter.Radiobutton(
        window,
        text="Play against a computer",
        variable=gameMode,
        value="pve",
        font=("Times New Roman", 15),
    ).grid(row=1, column=0, padx=15, pady=15, sticky=tkinter.W)

    tkinter.Radiobutton(
        window,
        text="Play online",
        variable=gameMode,
        value="online",
        font=("Times New Roman", 15),
    ).grid(row=2, column=0, padx=15, pady=15, sticky=tkinter.W)

    tkinter.Label(
        window,
        text="(Incase of online mode) Enter ip address and port in format - ip:port like (255.255.255.255:2137)",
        font=("Times New Roman", 15, "italic"),
    ).grid(row=3, column=0, padx=15, pady=15, sticky=tkinter.W)

    onlineEntry = tkinter.Entry(window, font=("Times New Roman", 15, "italic"))
    onlineEntry.grid(
        row=4, column=0, padx=15, pady=15, ipadx=20, ipady=5, sticky=tkinter.W
    )

    tkinter.Label(
        window,
        text="(Incase of online mode) Choose side",
        font=("Times New Roman", 15, "italic"),
    ).grid(row=5, column=0, padx=15, pady=15, sticky=tkinter.W)

    side = tkinter.StringVar(value="server")
    tkinter.Radiobutton(
        window,
        text="Server",
        variable=side,
        value="server",
        font=("Times New Roman", 15),
    ).grid(row=6, column=0, padx=15, pady=15, sticky=tkinter.W)

    tkinter.Radiobutton(
        window,
        text="Client",
        variable=side,
        value="client",
        font=("Times New Roman", 15),
    ).grid(row=7, column=0, padx=15, pady=15, sticky=tkinter.W)

    tkinter.Button(
        window,
        text="Play",
        font=("Times New Roman", 20, "italic"),
        command=lambda: playGame(window, side.get(), gameMode.get(), onlineEntry.get()),
    ).grid(row=8, column=0, padx=15, pady=15, ipadx=20, ipady=5)

    window.mainloop()


if __name__ == "__main__":
    main()
