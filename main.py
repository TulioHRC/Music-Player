from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from functions import music as audio
from functions import files as files
from functions.scrollbar import createScrollableFrame
from html import unescape
import random

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.master.iconbitmap('./images/music-logo.ico')
        self.sizes = [self.master.winfo_screenwidth(), self.master.winfo_screenheight()]
        self.master.geometry(f"{int(self.sizes[0]*0.8)}x{int(self.sizes[1]*0.8)}+{int(self.sizes[0]*0.1)}+{int(self.sizes[1]*0.1)}")
        self.master.resizable(0,0)
        self.master.config(background="Gray") # Like a border

        # Important variables
        self.playing = 0
        self.volume = 50
        self.music = ''
        self.musicsList = []
        self.backupList = []
        self.randomized = 0

        # Frames
        self.menu = Frame(self.master)
        self.menu.pack()
        self.menu.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8)),
                            width=str(int(self.sizes[0]*0.8*0.2)), relx=0, rely=0)
        self.menu.config(background="#151a24")
        self.menuConstruct()

        self.stuffConstruct()

        self.player = Frame(self.master)
        self.player.pack()
        self.player.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2)),
                            width=str(int(self.sizes[0]*0.8*0.8)), relx=0.2, rely=0.8)
        self.player.config(background="#000000")
        self.playerConstruct()

    def menuConstruct(self, selected="all"):
        menuSymbol = Label(self.menu, text=unescape("&#9776;"), bg="Black", fg="White", height="1", font=('Arial', 16))
        menuSymbol.pack(fill="x")

        self.all = Button(self.menu, text="All Songs", bg="Black", fg="White", height="1")
        self.all.config(font=('Arial', 16), highlightbackground="White", highlightcolor="White")
        self.all.pack(fill="x")

        self.recent = Button(self.menu, text="Recent Added", bg="Black", fg="White", height="1")
        self.recent.config(font=('Arial', 16), highlightbackground="White", highlightcolor="White")
        self.recent.pack(fill="x")

        if selected == "all": self.all.config(bg="Gray")
        elif selected == "recent": self.recent.config(bg="Gray")

        Label(self.menu, text="Playlists", bg="Black", fg="White", height="5", font=('Arial', 20),
                    highlightbackground="White", highlightcolor="White").pack(fill="x")

        # For with the playlists

    def stuffConstruct(self): # Will be "reconstructed" many times
        self.mainStuff = Frame(self.master)
        self.mainStuff.pack()
        self.mainStuff.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.8)),
                            width=str(int(self.sizes[0]*0.8*0.8)), relx=0.2, rely=0)

        self.stuff = createScrollableFrame(self.mainStuff)
        self.stuff.config(background="#353638")

        # Image loading
        path = r"./images/all Songs.jpg"
        img = ImageTk.PhotoImage(Image.open(path).resize((int(self.sizes[0]*0.8*0.75), int(self.sizes[1]*0.8*0.2)), Image.ANTIALIAS))
        panel = Label(self.stuff, image=img, border="0.1")
        panel.photo = img
        panel.pack()

        self.musicsList = files.findMusics()
        self.musicsWidgets = {}
        for n in range(0, len(self.musicsList)):
            self.musicsWidgets[f"{self.musicsList[n]}"] = Button(self.stuff, text=self.musicsList[n], font=('Arial', 12),
                                    command=lambda i=self.musicsList[n]: self.playM(i), bg="Black", fg="White",
                                    width=75, height=1)
            self.musicsWidgets[f"{self.musicsList[n]}"].pack()


    def playerConstruct(self):
        self.name = Label(self.player, text="", border="0", fg="White")
        self.name.config(font=('Arial', 12), background='#000000')
        self.name.pack()
        self.name.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.3)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.4)), relx=0.025, rely=0)

        self.before = Button(self.player, text=unescape('&#9664;&#9664;'), border="0", fg="White",
                                font=('MS Sans Serif', 36), background='#000000', command=lambda: self.change(-1))
        self.before.pack()
        self.before.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.05, rely=0.3)

        self.play = Button(self.player, text=unescape('&#9654;'), command=lambda: self.playM('', 1), border="0", fg="White")
        self.play.config(font=('MS Sans Serif', 36), background='#000000')
        self.play.pack()
        self.play.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.125, rely=0.3)

        self.forward = Button(self.player, text=unescape('&#9654;&#9654;'), border="0", fg="White")
        self.forward.config(font=('MS Sans Serif', 36), background='#000000', command=lambda: self.change(1))
        self.forward.pack()
        self.forward.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.2, rely=0.3)

        img = ImageTk.PhotoImage(Image.open(r"./images/shuffle.png").resize((int(self.sizes[0]*0.8*0.8*0.04),
                                        int(self.sizes[1]*0.8*0.2*0.25)), Image.ANTIALIAS))
        self.random = Button(self.player, image=img, fg="white", bg="black", border="0", command=self.randomize)
        self.random.photo = img
        self.random.pack()
        self.random.place(bordermode=OUTSIDE, anchor="nw", relx=0.66, rely=0.375)

        self.volumeS = Scale(self.player, from_=0, to=100, orient=HORIZONTAL, fg='white', bg='#000000'
                                , command=audio.volume, variable=self.volume)
        self.volumeS.pack()
        self.volumeS.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.2)), relx=0.75, rely=0.3)
        self.volumeS.set(50)


    def check(self):
        # Check if the music is playing or not (to auto advance to the next music)
        if self.playing == 1 and audio.checkMusic() == 0:
            self.change(1)
        if self.playing != 0:
            root.after(1000, self.check)

    def playM(self, path='', firstTime=0):
        if not path:
            if firstTime==1:
                path = self.musicsList[0]
            else:
                path = self.music

        try:
            unpause = 0
            self.playing = 1
            # If the music is the same that the one was playing
            if self.music == path: # Put the music selected
                unpause = 1

            audio.playMusic(f"./musics/{path}.mp3", unpause)

            self.music =path # Put the music selected

            # Changing Button and others widgets
            self.play["text"] = unescape(' &#9612;&#9612;')
            self.play["command"] = self.pause
            self.play.config(font=('MS Sans Serif', 22))

            self.name["text"] = self.music

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
            self.play.config(font=('MS Sans Serif', 36))
        except Exception as e:
            messagebox.showerror('Error', f'A error has happened:\n{e}')

    def change(self, factor):
        try:
            self.pause()
            positionNow = self.musicsList.index(self.music) + factor # Next/before Position
            if(positionNow == len(self.musicsList)):
                self.playM(self.musicsList[0])
            elif(positionNow == -1):
                self.playM(self.musicsList[-1])
            else:
                self.playM(self.musicsList[positionNow])
        except Exception as e:
            messagebox.showerror('Error', f'A error has happened:\n{e}')

    def randomize(self):
        # Randomize self.musicsList
        if self.randomized == 0:
            self.randomized = 1
            self.backupList = self.musicsList.copy()
            random.shuffle(self.musicsList)

            self.random.destroy()
            img = ImageTk.PhotoImage(Image.open(r"./images/shuffle activated.png").resize((int(self.sizes[0]*0.8*0.8*0.04),
                                            int(self.sizes[1]*0.8*0.2*0.25)), Image.ANTIALIAS))
            self.random = Button(self.player, image=img, fg="white", bg="black", border="0", command=self.randomize)
            self.random.photo = img
            self.random.pack()
            self.random.place(bordermode=OUTSIDE, anchor="nw", relx=0.66, rely=0.375)
        else:
            self.randomized = 0
            self.musicsList = self.backupList

            self.random.destroy()
            img = ImageTk.PhotoImage(Image.open(r"./images/shuffle.png").resize((int(self.sizes[0]*0.8*0.8*0.04),
                                            int(self.sizes[1]*0.8*0.2*0.25)), Image.ANTIALIAS))
            self.random = Button(self.player, image=img, fg="white", bg="black", border="0", command=self.randomize)
            self.random.photo = img
            self.random.pack()
            self.random.place(bordermode=OUTSIDE, anchor="nw", relx=0.66, rely=0.375)



def main():
    global app, root

    root = Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    print('Running...')
    main()
