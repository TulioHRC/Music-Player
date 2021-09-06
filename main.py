from tkinter import *
from functions import music as audio

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.master.iconbitmap('./images/music-logo.ico')

        self.play = Button(text="Play Song", command=lambda: audio.playMusic(r".\musics\_Remake - Lofi music..._70k.mp3"))
        self.play.grid(row=0, column=0)


def main():
    global app, root

    root = Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    print('Running...')
    main()
