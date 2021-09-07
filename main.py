from tkinter import *
from tkinter import messagebox
from functions import music as audio
from html import unescape

SymBack = unescape('&#9664;&#9664;')
SymFow = unescape('&#9654;&#9654;') # Use them outside of the variable, to not save them

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.master.iconbitmap('./images/music-logo.ico')

        # Important variables
        self.playing = 0
        self.music = ''

        self.play = Button(text=unescape('&#9654;'), command=self.play)
        self.play.grid(row=0, column=0)

        self.pause = Button(text=unescape('  &#9612;&#9612;'), command=self.pause)
        self.pause.grid(row=0, column=1)

    def check(self):
        # Check if the music is playing or not (to auto advance to the next music)
        if self.playing == 1 and audio.checkMusic() == 0:
            print('Nothing playing...') # Put the advance function
        if self.playing != 0:
            root.after(1000, self.check)

    def play(self):
        try:
            unpause = 0
            self.playing = 1
            # If the music is the same that the one was playing
            if self.music == r".\musics\_Remake - Lofi music..._70k.mp3": # Put the music selected
                unpause = 1

            audio.playMusic(r".\musics\_Remake - Lofi music..._70k.mp3", unpause)

            self.music = r".\musics\_Remake - Lofi music..._70k.mp3" # Put the music selected
            self.check() # Starts the loop of checking
        except Exception as e:
            messagebox.showerror('Error', f"A error has happened:\n{e}")

    def pause(self):
        try:
            self.playing = 0
            audio.pauseMusic()

            self.music = r".\musics\_Remake - Lofi music..._70k.mp3" # Put the music selected
        except Exception as e:
            messagebox.showerror('Error', f'A error has happened:\n{e}')


def main():
    global app, root

    root = Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    print('Running...')
    main()
