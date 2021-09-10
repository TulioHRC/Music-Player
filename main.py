from tkinter import *
from tkinter import messagebox, font
from functions import music as audio
from html import unescape

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.master.iconbitmap('./images/music-logo.ico')
        self.sizes = [self.master.winfo_screenwidth(), self.master.winfo_screenheight()]
        self.master.geometry(f"{int(self.sizes[0]*0.8)}x{int(self.sizes[1]*0.8)}+{int(self.sizes[0]*0.1)}+{int(self.sizes[1]*0.1)}")
        self.master.resizable(0,0)
        self.master.config(background="Black") # Like a border

        # Frames
        self.menu = Frame(self.master)
        self.menu.pack()
        self.menu.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8)),
                            width=str(int(self.sizes[0]*0.8*0.2)), relx=0, rely=0)
        self.menu.config(background="Gray")

        self.stuff = Frame(self.master)
        self.stuff.pack()
        self.stuff.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.8)),
                            width=str(int(self.sizes[0]*0.8*0.8)), relx=0.2, rely=0)
        self.stuff.config(background="Yellow")

        self.player = Frame(self.master)
        self.player.pack()
        self.player.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2)),
                            width=str(int(self.sizes[0]*0.8*0.8)), relx=0.2, rely=0.8)
        self.player.config(background="Green")
        self.playerConstruct()

        # Important variables
        self.playing = 0
        self.music = ''

    def playerConstruct(self):
        print(font.families())
        self.before = Button(self.player, text=unescape('&#9664;&#9664;'), border="0")
        self.before.config(font=('MS Sans Serif', 26), background='Green')
        self.before.pack()
        self.before.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.05, rely=0.3)

        self.play = Button(self.player, text=unescape('&#9654;'), command=self.playM, border="0")
        self.play.config(font=('MS Sans Serif', 26), background='Green')
        self.play.pack()
        self.play.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.125, rely=0.3)

        self.forward = Button(self.player, text=unescape('&#9654;&#9654;'), border="0")
        self.forward.config(font=('MS Sans Serif', 26), background='Green')
        self.forward.pack()
        self.forward.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.2, rely=0.3)


    def check(self):
        # Check if the music is playing or not (to auto advance to the next music)
        if self.playing == 1 and audio.checkMusic() == 0:
            print('Nothing playing...') # Put the advance function
        if self.playing != 0:
            root.after(1000, self.check)

    def playM(self):
        try:
            unpause = 0
            self.playing = 1
            # If the music is the same that the one was playing
            if self.music == r".\musics\_Remake - Lofi music..._70k.mp3": # Put the music selected
                unpause = 1

            audio.playMusic(r".\musics\_Remake - Lofi music..._70k.mp3", unpause)

            self.music = r".\musics\_Remake - Lofi music..._70k.mp3" # Put the music selected

            # Changing Button
            self.play["text"] = unescape(' &#9612;&#9612;')
            self.play["command"] = self.pause

            self.check() # Starts the loop of checking
        except Exception as e:
            messagebox.showerror('Error', f"A error has happened:\n{e}")

    def pause(self):
        try:
            self.playing = 0
            audio.pauseMusic()

            # Changing Button
            self.play["text"] = unescape('&#9654;')
            self.play["command"] = self.playM

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
