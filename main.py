from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from functions import music as audio
from functions import files
from functions.scrollbar import createScrollableFrame
from functions import playlists as playlist
from functions import conversor
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
        self.musicPos = 0
        self.music = ''
        self.musicsList = []
        self.playlists = playlist.loadPlaylists()
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

        # Keyboards shortcuts
        self.master.bind("<space>", self.space)

    def menuConstruct(self):
        menuSymbol = Label(self.menu, text=unescape("&#9776;"), bg="Black", fg="White", height="1", font=('Arial', 16))
        menuSymbol.pack(fill="x")

        self.all = Button(self.menu, text="All Songs", bg="Black", fg="White", height="1", command=lambda: self.stuffConstruct(order="char", reCreate=1))
        self.all.config(font=('Arial', 16), highlightbackground="White", highlightcolor="White")
        self.all.pack(fill="x")

        self.recent = Button(self.menu, text="By Date", bg="Black", fg="White", height="1", command=lambda: self.stuffConstruct(order="date", reCreate=1))
        self.recent.config(font=('Arial', 16), highlightbackground="White", highlightcolor="White")
        self.recent.pack(fill="x")

        Label(self.menu, text="Playlists", bg="Black", fg="White", height="5", font=('Arial', 20),
                    highlightbackground="White", highlightcolor="White").pack(fill="x")

        # Playlists
        self.add = Button(self.menu, text="+ Playlist", bg="Black", fg="Gray", height="1", command=AddPlaylist)
        self.add.config(font=('Arial', 16), highlightbackground="White", highlightcolor="White")
        self.add.pack(fill="x")

        # For with the playlists
        self.playButtons = []
        for i in range(0, len(self.playlists[0])):
            self.playButtons.append(Button(self.menu, text=f"{self.playlists[0][i]}", bg="Black", fg="White", height="1", command=lambda i=i: self.stuffConstruct(self.playlists[0][i], reCreate=1))) # , command=AddPlaylist)
            self.playButtons[i].config(font=('Arial', 16), highlightbackground="White", highlightcolor="White")
            self.playButtons[i].pack(fill="x")


    def stuffConstruct(self, playlistName="", order="char", reCreate=""): # Will be "reconstructed" many times
        if reCreate:
            try:
                self.mainStuff.destroy()
                self.stuff.destroy()
            except Exception as e:
                print(e)
                messagebox.showerror('Error', f"A error has happened:\n{e}")

        if not playlistName:
            if order=="char":
                self.recent.config(bg="Black")
                self.all.config(bg="Gray")
            else:
                self.recent.config(bg="Gray")
                self.all.config(bg="Black")
        else:
            self.menu.destroy()
            self.mainStuff.destroy()
            self.menu = Frame(self.master)
            self.menu.pack()
            self.menu.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8)),
                                width=str(int(self.sizes[0]*0.8*0.2)), relx=0, rely=0)
            self.menu.config(background="#151a24")
            self.menuConstruct()


            # Else playlist (put the colors on the playlists List)

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
        panel.grid(row=0, column=0, columnspan=2, pady=10)

        if playlistName:
            self.playlists = playlist.loadPlaylists()
            playlistPos = list(self.playlists[0]).index(playlistName)
            self.musicsList = files.findMusics(self.playlists[1][playlistPos], order)

            # Config buttons of playlist
            Button(self.stuff, text="Edit Playlist", font=('Arial', 16), width=20, bg='#5379b5', fg="White",
                        command=lambda: AddPlaylist(playlistName)).grid(row=1, column=0)
            path = r"./images/trash.jpg"
            img = ImageTk.PhotoImage(Image.open(path).resize((int(self.sizes[0]*0.8*0.05), int(self.sizes[1]*0.8*0.08)), Image.ANTIALIAS))
            trash = Button(self.stuff, image=img, border="0.1", command=lambda i=playlistName: self.delete(playlistName))
            trash.photo = img
            trash.grid(row=1, column=1, pady = 10)
        else:
            self.musicsList = files.findMusics('', order)

        self.musicsWidgets = {}
        for n in range(0, len(self.musicsList)):
            try:
                self.musicsWidgets[f"{self.musicsList[n]}"] = Button(self.stuff, text=self.musicsList[n], font=('Arial', 12),
                                        command=lambda i=self.musicsList[n]: self.playM(i), bg="Black", fg="White",
                                        width=80, height=1)
                self.musicsWidgets[f"{self.musicsList[n]}"].grid(row=n+2, column=0, padx=10)

                path = r"./images/see more.png"
                img = ImageTk.PhotoImage(Image.open(path).resize((int(self.sizes[0]*0.8*0.05), int(self.sizes[1]*0.8*0.05)), Image.ANTIALIAS))
                panel = Button(self.stuff, image=img, border="0.1", command=lambda i=self.musicsList[n]: Edit(i))
                panel.photo = img
                panel.grid(row=n+2, column=1, padx=30)
            except Exception as e:
                print(f'There was an error to load the musics.\n{e}')

        Label(self.stuff, text="", height=1, bg="#353638").grid(row=len(self.musicsList)+2, column=0)
        Label(self.stuff, text="", height=1, bg="#353638").grid(row=len(self.musicsList)+3, column=0)


    def playerConstruct(self):
        self.name = Label(self.player, text="", border="0", fg="White")
        self.name.config(font=('Arial', 10), background='#000000')
        self.name.pack()
        self.name.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.3)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.45)), relx=0.05, rely=0)

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

        # Music Time position changer
        self.musicScale = Scale(self.player, from_=0, to=100, orient=HORIZONTAL, fg='#2e99db', bg='white'
                                , command=self.changePos, variable=self.musicPos, resolution=0.5,
                                state=DISABLED, troughcolor='#2e99db', showvalue=0)
        self.musicScale.pack()
        self.musicScale.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.2)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.35)), relx=0.28, rely=0.4)

        self.sTime = Label(self.player, text="00:00", bg='#000000', fg="gray")
        self.sTime.pack()
        self.sTime.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.1)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.26, rely=0.7)

        self.fTime = Label(self.player, text="00:00", bg='#000000', fg="gray")
        self.fTime.pack()
        self.fTime.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.1)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.6, rely=0.7)

        img = ImageTk.PhotoImage(Image.open(r"./images/shuffle.png").resize((int(self.sizes[0]*0.8*0.8*0.04),
                                        int(self.sizes[1]*0.8*0.2*0.25)), Image.ANTIALIAS))
        self.random = Button(self.player, image=img, fg="white", bg="black", border="0", command=self.randomize)
        self.random.photo = img
        self.random.pack()
        self.random.place(bordermode=OUTSIDE, anchor="nw", relx=0.66, rely=0.375)

        self.volumeLabel = Label(self.player, text="Volume", bg='#000000', fg="gray")
        self.volumeLabel.pack()
        self.volumeLabel.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.2)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.825, rely=0.2)

        self.volumeS = Scale(self.player, from_=0, to=100, orient=HORIZONTAL, fg='white', bg='#000000'
                                , command=audio.volume, variable=self.volume, showvalue=0)
        self.volumeS.pack()
        self.volumeS.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.2)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.2)), relx=0.75, rely=0.4)
        self.volumeS.set(50)


    def check(self, first=False):
        # Check if the music is playing or not (to auto advance to the next music)
        if self.playing == 1 and audio.checkMusic() == 0:
            if first:
                # If the VLC player had an error or the player hasn't started yet
                # print('It has happened a small player error, but we resolved it!')
                pass
            else:
                root.after(500, self.change(1))
        if self.playing != 0:
            if self.fTime['text'] == '00:00':
                self.fTime['text'] = conversor.secToTimer(audio.getTimes()[1])
            else:
                times = audio.getTimes()
                self.musicScale.set(round((times[0]*100/times[1]), 1))
            self.sTime['text'] = conversor.secToTimer(audio.getTimes()[0])
            root.after(1000, self.check)

    def playM(self, path='', firstTime=0):
        if not self.music:
            firstTime = 1
        if not path:
            if firstTime==1:
                path = self.musicsList[0]
            else:
                path = self.music

        try:
            unpause = 0
            self.playing = 1
            # If the music is the same that the one was playing
            if self.music == path:
                unpause = 1
            elif firstTime != 1:
                self.musicsWidgets[f"{self.music}"].config(bg="black")

            self.musicsWidgets[f"{path}"].config(bg="gray")

            audio.playMusic(f"./musics/{path}.mp3", unpause, firstTime)

            self.music = path # Put the music selected

            # Changing Button and others widgets
            self.play["text"] = unescape(' &#9612;&#9612;')
            self.play["command"] = self.pause
            self.play.config(font=('MS Sans Serif', 22))

            self.name["text"] = self.music

            if firstTime:
                audio.volume(self.volumeS.get())

            self.fTime['text'] = '00:00' # Restarting fTime
            self.musicScale['state'] = 'active'

            root.after(1000, self.check(first=True)) # Starts the loop of checking
        except Exception as e:
            messagebox.showerror('Error', f"A error has happened:\n{e}")
            self.master.destroy()

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

    def space(self, event):
        self.play.invoke()

    def delete(self, name):
        try:
            r = messagebox.askyesno("Deleting Playlist", "You are going to delete this playlist. Are you sure?")
            if r:
                playlist.deletePlaylist(name)

                app.master.destroy() # Restart app
                main()
        except Exception as e:
            print(e)

    def changePos(self, value):
        times = audio.getTimes()
        actual = round((times[0]*100/times[1]), 1)
        if (float(value)-actual) > 2.5 or (float(value)-actual) < -2.5: # If changed sufficient
            audio.changeMusicPosition(times[1]*(float(value)/100)*1000)

class Edit(MainApp):
    def __init__(self, music):
        self.screen = Toplevel()
        self.screen.title("Edit")
        self.screen.grab_set()
        self.screen.iconbitmap('./images/music-logo.ico')
        self.screen.geometry(f"{int(app.sizes[0]*0.8*0.4)}x{int(app.sizes[1]*0.8*0.3)}+{int(app.sizes[0]*0.1)}+{int(app.sizes[1]*0.1)}")
        self.screen.resizable(0,0)
        self.music = music

        self.initFrame()

    def initFrame(self):
        try:
            self.frame.destroy()
        except:
            pass
        self.frame = Frame(self.screen)
        self.frame.pack(fill=BOTH, expand=True)
        self.frame.config(bg="Black")

        Label(self.frame, text=f"{self.music}", font=('Arial', 8), fg="White", bg="Black").pack(pady=5, padx=10, fill=X, expand=True)
        Button(self.frame, text="Rename", font=('Arial', 15), fg="White", bg="Black",
                    command=self.renameFrame).pack(pady=5, padx=10, fill=X, expand=True)
        Button(self.frame, text="Delete", font=('Arial', 15), fg="White", bg="Black",
                    command=self.delete).pack(pady=5, padx=10, fill=X, expand=True)
        Button(self.frame, text="Information", font=('Arial', 15), fg="White", bg="Black").pack(pady=5, padx=10, fill=X, expand=True)

    def renameFrame(self):
        self.frame.destroy()
        self.frame = Frame(self.screen)
        self.frame.pack(fill=BOTH, expand=True)
        self.frame.config(bg="Black")

        img = ImageTk.PhotoImage(Image.open(r"./images/back.jpg").resize((int(app.sizes[0]*0.8*0.8*0.04),
                                        int(app.sizes[1]*0.8*0.2*0.25)), Image.ANTIALIAS))
        self.back = Button(self.frame, image=img, border="0", fg="White", bg="Black", command=self.initFrame)
        self.back.photo = img
        self.back.pack(pady=1, padx=10, fill=X, expand=True)
        Label(self.frame, text=f"{self.music}", font=('Arial', 8), fg="White", bg="Black").pack(pady=5, padx=10, fill=X, expand=True)
        self.newName = Entry(self.frame, font=('Arial', 18))
        self.newName.pack(pady=5, padx=10, fill=X, expand=True)
        Button(self.frame, text="Rename Music", font=('Arial', 18), fg="White", bg="Black",
                    command=lambda: self.rename(self.newName.get())).pack(pady=5, padx=10, fill=X, expand=True)

    def rename(self, name):
        try:
            files.renameMusic(self.music, name)
            messagebox.showinfo('Succeed', f'We changed the {self.music} to {name}!\nNow we are restarting the application...')
            app.master.destroy()
            main()
        except Exception as e:
            messagebox.showerror('Error', f'There was an error to rename the music.\n{e}')

    def delete(self):
        try:
            r = messagebox.askyesno('Delete', f'Are you sure to delete {self.music}?')
            if r:
                files.deleteMusic(self.music)
                messagebox.showinfo('Succeed', f'We deleted {self.music}!\nNow we are restarting the application...')
                app.master.destroy()
                main()
        except Exception as e:
            messagebox.showerror('Error', f'There was an error when we were trying to delete you music.\n{e}')

class AddPlaylist(MainApp):
    def __init__(self, editPlaylist=False):
        self.screen = Toplevel()
        self.screen.title("Add new Playlist")
        if editPlaylist:
            self.screen.title(f"Edit {editPlaylist} Playlist")
        self.screen.grab_set()
        self.screen.iconbitmap('./images/music-logo.ico')
        self.screen.geometry(f"{int(app.sizes[0]*0.8*0.35)}x{int(app.sizes[1]*0.8*0.6)}+{int(app.sizes[0]*0.1)}+{int(app.sizes[1]*0.1)}")
        self.screen.resizable(0,0)
        self.screen.config(bg="Black")

        self.musics = files.findMusics()
        self.playlistEdit = editPlaylist

        if not editPlaylist:
            Label(self.screen, text="Name: ", fg="White", bg="Black").grid(row=0, column=0, padx=10, pady=15)
            self.name = Entry(self.screen, width=35)
            self.name.grid(row=0, column=1)

        self.box = Listbox(self.screen, height=12, width=40, selectmode=MULTIPLE, font="size=8")
        self.box.grid(row=1, column=0, columnspan=2, padx=10, pady=15)
        for music in self.musics:
            self.box.insert(END, music)

        if editPlaylist:
            # List of already musics in the playlist
            self.playlists = playlist.loadPlaylists()
            self.musicsList = files.findMusics(self.playlists[1][list(self.playlists[0]).index(editPlaylist)])

            self.box.selection_clear(0, END)
            for music in self.musicsList:
                self.pos = self.musics.index(music)
                self.box.selection_set(self.pos)
                self.box.activate(self.pos)

            Button(self.screen, text="Edit", command=self.edit, width=30).grid(row=2, column=0, columnspan=2, padx=10, pady=15)
        else:
            Button(self.screen, text="Create", command=self.create, width=30).grid(row=2, column=0, columnspan=2, padx=10, pady=15)

    def create(self):
        try:
            name = self.name.get()
            musicsPoses = self.box.curselection()
            musics = []
            self.playlists = playlist.loadPlaylists()

            if len(name) <= 2 or name in self.playlists[0]:
                int('A error has happened:\nThe name of the playlist is too short\n or this name has already being used!')
            else:
                for pos in musicsPoses:
                    musics.append(self.musics[pos])

                playlist.createPlaylist(name, musics)
                messagebox.showinfo('Succeed', 'The playlist was created!')
                self.screen.destroy()

                app.master.destroy() # Restart app
                main()
        except Exception as e:
            messagebox.showerror('Error', f"A error has happened:\n{e}")

    def edit(self):
        try:
            musicsPoses = self.box.curselection()
            musics = []
            self.playlists = playlist.loadPlaylists()

            for pos in musicsPoses:
                musics.append(self.musics[pos])

            playlist.updatePlaylist(self.playlistEdit, musics)
            messagebox.showinfo('Succeed', f'The playlist {self.playlistEdit} was edited!')
            self.screen.destroy()

            app.master.destroy() # Restart app
            main()
        except Exception as e:
            messagebox.showerror('Error', f"A error has happened:\n{e}")


def main():
    global app, root

    root = Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    print('Running...')
    main()
