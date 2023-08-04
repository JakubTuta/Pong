import re
import tkinter


def isValidIp(ip):
    pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}$"
    if re.match(pattern, ip) is not None:
        numbers = ip.split(".")
        for num in numbers:
            if not (0 <= int(num) <= 255):
                return False
        port = ip.split(":")[-1]
        if not (1 <= int(port) <= 9999):
            return False
        return True
    return False


def playGame(gameMode, inputIp):
    if gameMode == "pvp":
        # play vs player
        pass

    elif gameMode == "pve":
        # play vs computed
        pass

    else:
        if isValidIp(inputIp):
            return

        playerIp, playerPort = inputIp.split(":")
        pass


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
        text="(Incase of online mode) Enter ip address and port in format - ip:port (255.255.255.255:2137)",
        font=("Times New Roman", 15, "italic"),
    ).grid(row=3, column=0, padx=15, pady=15, sticky=tkinter.W)

    onlineEntry = tkinter.Entry(window, font=("Times New Roman", 15, "italic"))
    onlineEntry.grid(row=4, column=0, padx=15, pady=15, sticky=tkinter.W)

    tkinter.Button(
        window, text="Play", command=lambda: playGame(gameMode.get(), onlineEntry.get())
    )

    window.mainloop()


if __name__ == "__main__":
    main()
