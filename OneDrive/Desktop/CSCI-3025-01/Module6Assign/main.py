import tkinter as tk
from gameGui import gameGui


def main():
    window = tk.Tk()
    window.title("Escape from the Dungeon")
    window.geometry("480x680")
    window.resizable(False, False)

    game = gameGui(window, size=10)

    window.mainloop()


if __name__ == "__main__":
    main()