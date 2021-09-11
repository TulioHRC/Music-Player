from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
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
        self.master.config(background="Gray") # Like a border

        # Important variables
        self.playing = 0
        self.volume = 50
        self.music = ''

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
        self.stuff = Frame(self.master)
        self.stuff.pack()
        self.stuff.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.8)),
                            width=str(int(self.sizes[0]*0.8*0.8)), relx=0.2, rely=0)
        self.stuff.config(background="#353638")

        # Image loading
        path = r"./images/all Songs.jpg"
        img = ImageTk.PhotoImage(Image.open(path).resize((int(self.sizes[0]*0.8*0.75), int(self.sizes[1]*0.8*0.2)), Image.ANTIALIAS))
        panel = Label(self.stuff, image=img, border="0.1")
        panel.photo = img
        panel.pack()
        panel.place(bordermode=OUTSIDE, anchor="nw", relx=0.0175, rely=0)


    def playerConstruct(self):
        self.name = Label(self.player, text="", border="0", fg="White")
        self.name.config(font=('Arial', 12), background='#000000')
        self.name.pack()
        self.name.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.3)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.4)), relx=0.025, rely=0)

        self.before = Button(self.player, text=unescape('&#9664;&#9664;'), border="0", fg="White")
        self.before.config(font=('MS Sans Serif', 36), background='#000000')
        self.before.pack()
        self.before.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.05, rely=0.3)

        self.play = Button(self.player, text=unescape('&#9654;'), command=self.playM, border="0", fg="White")
        self.play.config(font=('MS Sans Serif', 36), background='#000000')
        self.play.pack()
        self.play.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.125, rely=0.3)

        self.forward = Button(self.player, text=unescape('&#9654;&#9654;'), border="0", fg="White")
        self.forward.config(font=('MS Sans Serif', 36), background='#000000')
        self.forward.pack()
        self.forward.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.2, rely=0.3)

        self.volumeS = Scale(self.player, from_=0, to=100, orient=HORIZONTAL, fg='white', bg='#000000'
                                , command=audio.volume, variable=self.volume)
        self.volumeS.pack()
        self.volumeS.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.2)), relx=0.75, rely=0.3)
        self.volumeS.set(50)


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
