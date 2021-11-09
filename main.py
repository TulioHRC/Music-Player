from tkinter import *
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
from functions import music as audio
from functions import files
from functions.scrollbar import createScrollableFrame
from functions import playlists as playlist
from functions import conversor
from html import unescape
import random

# Main class of the application
class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.master.iconbitmap('./images/music-logo.ico') # Logo icon
        self.sizes = [self.master.winfo_screenwidth(), self.master.winfo_screenheight()] # User monitor sizes
        self.master.geometry(f"{int(self.sizes[0]*0.8)}x{int(self.sizes[1]*0.8)}+{int(self.sizes[0]*0.1)}+{int(self.sizes[1]*0.1)}")
        self.master.resizable(0,0) # Disable modifying the size of the window
        self.master.config(background="Gray")

        # Important variables
        self.playing = 0 # If music is playing
        self.musicsList = []
        self.musicPos = 0 # Music position in the musics list
        self.music = ''
        self.preLoadedList = files.preLoad() # Pre load data
        self.volume = int(self.preLoadedList[2])
        self.playlists = playlist.loadPlaylists()
        self.posPlaylists = 0 # Which playlist is selected
        self.randomized = 0
        self.backupList = [] # Just a variable to help the app

        # Window Frames
        self.menu = Frame(self.master) # Menu frame
        self.menu.pack()
        self.menu.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8)),
                            width=str(int(self.sizes[0]*0.8*0.2)), relx=0, rely=0)
        self.menu.config(background="#151a24")
        self.menuConstruct()

        self.stuffConstruct() # Musics list frame

        self.player = Frame(self.master) # Player frame
        self.player.pack()
        self.player.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2)),
                            width=str(int(self.sizes[0]*0.8*0.8)), relx=0.2001, rely=0.801)
        # The decimals in the relx and rely are for give the player a "margin"
        self.player.config(background="#000000")
        self.playerConstruct()

        # Keyboards shortcuts
        self.master.bind("<space>", self.space) # When the space is pressed, the musics plays or pauses


    # Menu


    def menuConstruct(self, playlistName=''):
        menuSymbol = Label(self.menu, text=unescape("&#9776;"), bg="Black", fg="#2e99db", height="1", font=('Arial', 16))
        menuSymbol.pack(fill="x")

        self.all = Button(self.menu, text="All Songs", bg="Black", fg="White", height="1", command=lambda: self.stuffConstruct(order="char", reCreate=1))
        self.all.config(font=('Arial', 14), highlightbackground="White", highlightcolor="White")
        self.all.pack(fill="x")

        self.recent = Button(self.menu, text="By Date", bg="Black", fg="White", height="1", command=lambda: self.stuffConstruct(order="date", reCreate=1))
        self.recent.config(font=('Arial', 14), highlightbackground="White", highlightcolor="White")
        self.recent.pack(fill="x")

        Label(self.menu, text="Playlists", bg="Black", fg="White", height="3", font=('Arial', 18),
                    highlightbackground="White", highlightcolor="White").pack(fill="x", pady=2)

        # Playlists
        self.add = Button(self.menu, text="+ Playlist", bg="Black", fg="White", height="1", command=AddPlaylist)
        self.add.config(font=('Arial', 14), highlightbackground="White", highlightcolor="White")
        self.add.pack(fill="x")

        self.playlistsConstruct(playlistName, self.posPlaylists) # Load the playlists

        self.config = Button(self.menu, text=unescape('&#9881;'), bg="Black", fg="White", height="1",
                        command=Config, font=('Arial', 14), highlightbackground="White", highlightcolor="White")
        self.config.pack(fill="x", side=BOTTOM) # Settings

        self.restartBt = Button(self.menu, text=unescape('&#8634;'), bg="Black", fg="White", height="1",
                                command=self.restart, font=('Arial', 14), highlightbackground="White", highlightcolor="White")
        self.restartBt.pack(fill="x", side=BOTTOM) # Restart Application

    def restart(self): # Restart application function
        self.master.destroy()
        main()

    def playlistsConstruct(self, playlistName='', start=0): # Load playlists in the menu frame
        try:
            self.playlistsFrame.destroy()
        except:
            pass

        self.playlistsFrame = Frame(self.menu)
        self.playlistsFrame.pack(fill="x")

        up = Button(self.playlistsFrame, text=unescape('&#10506;'), bg="Black", fg="White",
                    command=lambda: self.changeMenuPosition(playlistName, -1))
        up.pack(fill="x", pady=1)
        if start == 0:
            up.config(state=DISABLED)

        # For with the playlists
        self.playButtons = []

        if len(self.playlists[0]) > (7+start): # If the number of playlists it's more than 7
            max = start + 7 # Last playlist that will apear
        else:
            max = len(self.playlists[0])

        for i in range(0, 7):
            self.playButtons.append(Button(self.playlistsFrame, text=f"{self.playlists[0][i+start]}", bg="Black", fg="White", height="1",
                                        command=lambda i=i: self.stuffConstruct(self.playlists[0][i+start], reCreate=1)))
            self.playButtons[i].config(font=('Arial', 12), highlightbackground="White", highlightcolor="White")
            if playlistName == self.playlists[0][i+start]: # If the playlist is selected put the gray color in background
                self.playButtons[i].config(bg="Gray")
            self.playButtons[i].pack(fill="x")

        if len(self.playlists[0]) > 7:
            down = Button(self.playlistsFrame, text=unescape('&#10507;'), bg="Black", fg="White",
                        command=lambda: self.changeMenuPosition(playlistName, 1))
            down.pack(fill="x", pady=1) # Down button, instead of up button
            if (start + 7) >= len(self.playlists[0]):
                down.config(state=DISABLED) # Down disabled if is nothing more down

    def changeMenuPosition(self, playlistName, change): # Up/Down functions
        self.posPlaylists += change
        self.playlistsConstruct(playlistName, self.posPlaylists)


    # Musics list frame


    def stuffConstruct(self, playlistName="", order="char", reCreate="", search=0): # Will be "reconstructed" many times
        mainPage = 0 # Will be 1 if it's the main music page

        if reCreate: # If needs to recreate the music list from scratch
            try:
                self.mainStuff.destroy()
                self.stuff.destroy()
            except Exception as e:
                print(e)
                messagebox.showerror('Error', f"A error has happened:\n{e}")

        # Playlist Colors
        if not playlistName:
            if order=="char": # Main page
                self.recent.config(bg="Black")
                self.all.config(bg="Gray")
                mainPage = 1 # Main music page
            else: # By date page
                self.recent.config(bg="Gray")
                self.all.config(bg="Black")

            for b in self.playButtons: # All playlists black (not selected)
                b.config(bg="Black")
        else: # Playlist selected
            self.menu.destroy()
            self.mainStuff.destroy()
            self.menu = Frame(self.master)
            self.menu.pack()
            self.menu.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8)),
                                width=str(int(self.sizes[0]*0.8*0.2)), relx=0, rely=0)
            self.menu.config(background="#151a24")
            self.menuConstruct(playlistName)

        self.mainStuff = Frame(self.master)
        self.mainStuff.pack()
        self.mainStuff.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.8)),
                            width=str(int(self.sizes[0]*0.8*0.8)), relx=0.2, rely=0)

        self.stuff = createScrollableFrame(self.mainStuff) # Adding scrollbar
        self.stuff.config(background="#353638")

        if playlistName:
            self.playlists = playlist.loadPlaylists()
            playlistPos = list(self.playlists[0]).index(playlistName)
            self.musicsList = files.findMusics(self.playlists[1][playlistPos], order, preData=self.preLoadedList)

            # Config buttons of playlist
            Button(self.stuff, text="Edit Playlist", font=('Arial', 16), width=20, bg='#5379b5', fg="White",
                        command=lambda: AddPlaylist(playlistName)).grid(row=1, column=0)
            path = r"./images/trash.jpg"
            img = ImageTk.PhotoImage(Image.open(path).resize((int(self.sizes[0]*0.8*0.05), int(self.sizes[1]*0.8*0.08)), Image.ANTIALIAS))
            trash = Button(self.stuff, image=img, border="0.1", command=lambda i=playlistName: self.delete(playlistName))
            trash.photo = img
            trash.grid(row=1, column=1, pady = 10)
        else:
            self.musicsList = files.findMusics('', order, preData=self.preLoadedList)
            if mainPage: # Search tools load
                self.search = Entry(self.stuff, font=('Arial', 18), width=52)
                self.search.grid(row=0, column=0, pady=30, padx=20)
                Button(self.stuff, text="Search", bg="black", fg="white", command=lambda:self.stuffConstruct(search=self.search.get()),
                    font=("Arial", 12), width=6, height=1).grid(row=0, column=1, pady=30, padx=20)
            else:
                Label(self.stuff, text="", height=1, bg="#353638").grid(row=0, column=0)
                Label(self.stuff, text="", height=1, bg="#353638").grid(row=1, column=0)

        # Musics load into the page
        self.musicsWidgets = {}
        for n in range(0, len(self.musicsList)):
            if search:
                if not search in self.musicsList[n]: # The search word isn't into the musics list
                    continue # Skips this song in the loop
            try: # Creating music widget
                i = n+2
                if not playlistName: i += 2
                self.musicsWidgets[f"{self.musicsList[n]}"] = Button(self.stuff, text=self.musicsList[n], font=('Arial', 12),
                                        command=lambda i=self.musicsList[n]: self.playM(i), bg="#141414", fg="White",
                                        width=76, height=1)
                self.musicsWidgets[f"{self.musicsList[n]}"].grid(row=i, column=0, padx=35)

                path = r"./images/see more.png"
                img = ImageTk.PhotoImage(Image.open(path).resize((int(self.sizes[0]*0.8*0.05), int(self.sizes[1]*0.8*0.05)), Image.ANTIALIAS))
                panel = Button(self.stuff, image=img, border="0.1", command=lambda i=self.musicsList[n]: Edit(i))
                panel.photo = img
                panel.grid(row=i, column=1, padx=20)
            except Exception as e:
                print(f'There was an error to load the musics.\n{e}')

        # Extra labels to avoid strange white bar
        Label(self.stuff, text="", height=1, bg="#353638").grid(row=len(self.musicsList)+4, column=0)
        Label(self.stuff, text="", height=1, bg="#353638").grid(row=len(self.musicsList)+5, column=0)


    # Player frame


    def playerConstruct(self):
        self.name = Label(self.player, text="", border="0", fg="White") # Music Name
        self.name.config(font=('Arial', 10), background='#000000')
        self.name.pack()
        self.name.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.3)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.45)), relx=0.05, rely=0)

        self.before = Button(self.player, text=unescape('&#9664;&#9664;'), border="0", fg="White", # <<
                                font=('MS Sans Serif', 36), background='#000000', command=lambda: self.change(-1))
        self.before.pack()
        self.before.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.05, rely=0.3)

        self.play = Button(self.player, text=unescape('&#9654;'), command=lambda: self.playM('', 1), border="0", fg="White")
        self.play.config(font=('MS Sans Serif', 36), background='#000000')
        self.play.pack()
        self.play.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.125, rely=0.3)

        self.forward = Button(self.player, text=unescape('&#9654;&#9654;'), border="0", fg="White") # >>
        self.forward.config(font=('MS Sans Serif', 36), background='#000000', command=lambda: self.change(1))
        self.forward.pack()
        self.forward.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.4)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.2, rely=0.3)

        # Music time position changer
        self.musicScale = Scale(self.player, from_=0, to=100, orient=HORIZONTAL, fg='#2e99db', bg='white'
                                , command=self.changePos, variable=self.musicPos, resolution=0.5,
                                state=DISABLED, troughcolor='#2e99db', showvalue=0)
        self.musicScale.pack()
        self.musicScale.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.2)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.35)), relx=0.28, rely=0.4)

        self.sTime = Label(self.player, text="00:00", bg='#000000', fg="gray") # Actual time
        self.sTime.pack()
        self.sTime.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.1)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.26, rely=0.7)

        self.fTime = Label(self.player, text="00:00", bg='#000000', fg="gray") # Full length
        self.fTime.pack()
        self.fTime.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.1)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.05)), relx=0.6, rely=0.7)

        # Random button
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

        self.volumeS = Scale(self.player, from_=0, to=100, orient=HORIZONTAL, fg='white', bg='#000000' # Volume scale
                                , command=audio.volume, variable=self.volume, showvalue=0)
        self.volumeS.pack()
        self.volumeS.place(bordermode=OUTSIDE, anchor="nw", height=str(int(self.sizes[1]*0.8*0.2*0.2)),
                            width=str(int(self.sizes[0]*0.8*0.8*0.2)), relx=0.75, rely=0.4)
        self.volumeS.set(self.volume) # Set predefined volume

    # Player functions
    def check(self, first=False):
        # Check if the music is playing or not (to auto advance to the next music)
        if self.playing == 1 and audio.checkMusic() == 0:
            if not first: # Load more slow to avoid errors
                root.after(500, self.change(1))

        if self.playing != 0: # If it's playing
            if self.fTime['text'] == '00:00': # Configure final time label
                self.fTime['text'] = conversor.secToTimer(audio.getTimes()[1])
            else:
                times = audio.getTimes()
                self.musicScale.set(round((times[0]*100/times[1]), 1))
            self.sTime['text'] = conversor.secToTimer(audio.getTimes()[0]) # Changes actual music time label
            root.after(1000, self.check)

    def playM(self, path='', firstTime=0): # Play music Function
        if not self.music: # If it's the first music played
            firstTime = 1
        if not path:
            if firstTime==1: path = self.musicsList[0] # First music
            else: path = self.music # Already playing some music

        try:
            unpause = 0
            self.playing = 1
            # If the music is the same that the one was playing
            if self.music == path:
                unpause = 1
            elif firstTime != 1:
                self.musicsWidgets[f"{self.music}"].config(bg="black")

            self.musicsWidgets[f"{path}"].config(bg="gray") # Gray background in the playing music

            audio.playMusic(f"{files.getRealPath(path, folders=self.preLoadedList[1][1])}\\{path}.mp3", unpause, firstTime) # Play music

            self.music = path # Save the music selected

            # Changing Button and others widgets
            self.play["text"] = unescape(' &#9612;&#9612;')
            self.play["command"] = self.pause
            self.play.config(font=('MS Sans Serif', 22))

            self.name["text"] = self.music

            if firstTime: audio.volume(self.volumeS.get()) # Define first volume in the app start

            self.fTime['text'] = '00:00' # Restarting final time label
            self.musicScale['state'] = 'active' # Activate the music scale feature

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

    def change(self, factor): # Change the music
        try:
            self.pause()
            positionNow = self.musicsList.index(self.music) + factor # Next/before Position
            if(positionNow == len(self.musicsList)):
                self.playM(self.musicsList[0]) # Play first music if position is after the last music
            elif(positionNow == -1):
                self.playM(self.musicsList[-1]) # Play last music if position is before the first music
            else:
                self.playM(self.musicsList[positionNow]) # Play other position
        except Exception as e:
            messagebox.showerror('Error', f'A error has happened:\n{e}')

    def randomize(self):
        # Randomize self.musicsList
        if self.randomized == 0: # Not randomized
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
        else: # Already randomized, gets back to the backup list
            self.randomized = 0
            self.musicsList = self.backupList

            self.random.destroy()
            img = ImageTk.PhotoImage(Image.open(r"./images/shuffle.png").resize((int(self.sizes[0]*0.8*0.8*0.04),
                                            int(self.sizes[1]*0.8*0.2*0.25)), Image.ANTIALIAS))
            self.random = Button(self.player, image=img, fg="white", bg="black", border="0", command=self.randomize)
            self.random.photo = img
            self.random.pack()
            self.random.place(bordermode=OUTSIDE, anchor="nw", relx=0.66, rely=0.375)

    def changePos(self, value): # Change music position in its time
        times = audio.getTimes()
        actual = round((times[0]*100/times[1]), 1)
        if (float(value)-actual) > 2.5 or (float(value)-actual) < -2.5: # If changed sufficient
            audio.changeMusicPosition(times[1]*(float(value)/100)*1000)

    # Other functions

    def space(self, event): # Keyboard function of space
        self.play.invoke()

    def delete(self, name): # Delete playlist
        try:
            r = messagebox.askyesno("Deleting Playlist", "You are going to delete this playlist. Are you sure?")
            if r:
                playlist.deletePlaylist(name)
                app.master.destroy() # Restart app
                main()
        except Exception as e:
            print(e)

    def putScreen(self,screen): # Put the screen in top of the computer window
        screen.withdraw()
        screen.deiconify() # Put

# Music config window

class Edit(MainApp):
    def __init__(self, music):
        self.screen = Toplevel()
        self.screen.title("Edit")
        self.screen.grab_set() # Defines as firstly window
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
        self.back = Button(self.frame, image=img, border="0", fg="White", bg="Black", command=self.initFrame) # Get back to the main config page
        self.back.photo = img
        self.back.pack(pady=1, padx=10, fill=X, expand=True)
        Label(self.frame, text=f"{self.music}", font=('Arial', 8), fg="White", bg="Black").pack(pady=5, padx=10, fill=X, expand=True)
        self.newName = Entry(self.frame, font=('Arial', 8))
        self.newName.pack(pady=5, padx=10, fill=X, expand=True)
        self.newName.insert(0, self.music)
        Button(self.frame, text="Rename Music", font=('Arial', 18), fg="White", bg="Black",
                    command=lambda: self.rename(self.newName.get())).pack(pady=5, padx=10, fill=X, expand=True)

    def rename(self, name): # Rename music function
        try:
            files.renameMusic(self.music, name)
            messagebox.showinfo('Succeed', f'We changed the {self.music} to {name}!\nNow we are restarting the application...')
            app.master.destroy()
            main()
        except Exception as e:
            messagebox.showerror('Error', f'There was an error to rename the music.\n{e}')

    def delete(self): # Delete music function
        try:
            r = messagebox.askyesno('Delete', f'Are you sure to delete {self.music}?')
            if r:
                files.deleteMusic(self.music)
                messagebox.showinfo('Succeed', f'We deleted {self.music}!\nNow we are restarting the application...')
                app.master.destroy()
                main()
        except Exception as e:
            messagebox.showerror('Error', f'There was an error when we were trying to delete you music.\n{e}')

# Create playlist Frame

class AddPlaylist(MainApp):
    def __init__(self, editPlaylist=False):
        self.screen = Toplevel()
        self.screen.title("Add new Playlist")
        if editPlaylist: # If it's a edit playlist frame
            self.screen.title(f"Edit {editPlaylist} Playlist")
        self.screen.grab_set()
        self.screen.iconbitmap('./images/music-logo.ico')
        self.screen.geometry(f"{int(app.sizes[0]*0.8*0.35)}x{int(app.sizes[1]*0.8*0.6)}+{int(app.sizes[0]*0.1)}+{int(app.sizes[1]*0.1)}")
        self.screen.resizable(0,0)
        self.screen.config(bg="Black")

        self.musics = files.findMusics(preData=app.preLoadedList)
        self.playlistEdit = editPlaylist

        if not editPlaylist:
            Label(self.screen, text="Name: ", fg="White", bg="Black").grid(row=0, column=0, padx=10, pady=15)
            self.name = Entry(self.screen, width=35)
            self.name.grid(row=0, column=1)

        # List of all musics
        self.box = Listbox(self.screen, height=12, width=40, selectmode=MULTIPLE, font="size=8")
        self.box.grid(row=1, column=0, columnspan=2, padx=10, pady=15)
        for music in self.musics:
            self.box.insert(END, music)

        if editPlaylist:
            # List of already musics in the playlist
            self.playlists = playlist.loadPlaylists()
            self.musicsList = files.findMusics(self.playlists[1][list(self.playlists[0]).index(editPlaylist)], preData=app.preLoadedList)

            self.box.selection_clear(0, END)
            for music in self.musicsList:
                # Select already in playlist musics
                self.pos = self.musics.index(music)
                self.box.selection_set(self.pos)
                self.box.activate(self.pos)

            Button(self.screen, text="Edit", command=self.edit, width=30).grid(row=2, column=0, columnspan=2, padx=10, pady=15)
        else:
            Button(self.screen, text="Create", command=self.create, width=30).grid(row=2, column=0, columnspan=2, padx=10, pady=15)

    def create(self): # Create the playlist
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

    def edit(self): # Edit the playlist
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

# Configuration Frame

class Config(MainApp):
    def __init__(self):
        self.screen = Toplevel()
        self.screen.title('Configuration')
        self.screen.iconbitmap('./images/music-logo.ico')
        self.screen.geometry(f"{int(app.sizes[0]*0.5)}x{int(app.sizes[1]*0.6)}+{int(app.sizes[0]*0.2)}+{int(app.sizes[1]*0.2)}")
        self.screen.resizable(0,0)

        self.tabs = ttk.Notebook(self.screen)
        self.tabs.pack(fill=BOTH, expand=True)

        self.general()
        self.musicsFolder()

    def general(self): # Geral informartion Frame
        self.vDef = IntVar()

        self.generalFrame = Frame(self.tabs, bg="gray")
        self.generalFrame.pack(fill=BOTH, expand=True)
        self.tabs.add(self.generalFrame, text="General Config")

        # Default Volume
        self.volumeLabel = Label(self.generalFrame, text="Default Volume:", font=('Arial', 12), bg='#ababab', fg='White')
        self.volumeLabel.pack()
        self.volumeLabel.place(bordermode=OUTSIDE, anchor="nw", height=str(int(app.sizes[1]*0.6*0.1)),
                            width=str(int(app.sizes[0]*0.5*0.2)), relx=0.01, rely=0.05)
        self.volScale = Scale(self.generalFrame, from_=0, to=100, orient=HORIZONTAL, fg='white', bg='gray'
                                , variable=self.vDef)
        self.volScale.pack()
        self.volScale.place(bordermode=OUTSIDE, anchor="nw", height=str(int(app.sizes[1]*0.6*0.1)),
                            width=str(int(app.sizes[0]*0.5*0.25)), relx=0.26, rely=0.05)
        self.vDef.set(app.preLoadedList[2]) # Get pre volume saved

        # Theme
        self.themeLabel = Label(self.generalFrame, text="Theme:", font=('Arial', 12), bg='#ababab', fg='White')
        self.themeLabel.pack()
        self.themeLabel.place(bordermode=OUTSIDE, anchor="nw", height=str(int(app.sizes[1]*0.6*0.1)),
                            width=str(int(app.sizes[0]*0.5*0.2)), relx=0.01, rely=0.2)
        # List box

        # Restaure button
        self.restaureButton = Button(self.generalFrame, text="Restaure default settings", command=self.restaure, font=('Arial', 11), bg='#b5ac02', fg='white')
        self.restaureButton.pack()
        self.restaureButton.place(bordermode=OUTSIDE, anchor="nw", height=str(int(app.sizes[1]*0.6*0.075)),
                                width=str(int(app.sizes[0]*0.5*0.3)), relx=0.58, rely=0.905)

        # Apply button
        self.apply = Button(self.generalFrame, text="Apply", command=self.save, font=('Arial', 11), bg='#41b000', fg='white')
        self.apply.pack()
        self.apply.place(bordermode=OUTSIDE, anchor="nw", height=str(int(app.sizes[1]*0.6*0.075)),
                        width=str(int(app.sizes[0]*0.5*0.1)), relx=0.89, rely=0.905)

    def save(self): # Save configurations
        try:
            files.saveVolume(self.vDef.get())
            messagebox.showinfo('Saved', 'Default informations are saved now.')
        except Exception as e:
            messagebox.showerror('Error', f'Default informations not saved.\n{e}')

    def restaure(self): # Restaure to default configurations
        self.vDef.set(50)
        self.save() # Change to save all configs function

    def musicsFolder(self): # Music folders frame
        self.musicFrame = Frame(self.tabs, bg="gray")
        self.musicFrame.pack(fill=BOTH, expand=True)
        self.tabs.add(self.musicFrame, text="Music Folders")

        Label(self.musicFrame, text="Add Folders", font=('Arial', 14), bg="Gray", fg="Black").grid(row=0, column=0, columnspan=2, pady=15)

        Label(self.musicFrame, text="Name: ", font=('Arial', 11), bg="gray", fg="white").grid(row=1, column=0, pady=2, padx=1)
        self.name = Entry(self.musicFrame)
        self.name.grid(row=1, column=1, pady=2, padx=1)

        Label(self.musicFrame, text="Local address: ", font=('Arial', 11), bg="gray", fg="white").grid(row=2, column=0, pady=2, padx=1)
        self.local = Entry(self.musicFrame)
        self.local.grid(row=2, column=1, pady=2, padx=1)
        Button(self.musicFrame, text="Find folder", font=('Arial', 10), bg="Black", fg="White",
                    command=self.findFolder).grid(row=2, column=2, pady=2, padx=3)

        Button(self.musicFrame, text="Create", font=('Arial', 10), bg="Black", fg="White",
                    command=lambda: self.addFolder(self.name.get(), self.local.get())).grid(row=3, column=1, pady=2, padx=4)

        # View Actual Folders
        Label(self.musicFrame, text="Folders", font=('Arial', 14), bg="Gray", fg="Black").grid(row=0, column=4, pady=15)
        folds = files.readFolders()
        self.list = Frame(self.musicFrame, highlightbackground="black", highlightthickness=1, bg="White")
        self.list.grid(row=1, column=3, columnspan=3, pady=5, padx=15)
        if len(folds[0]) != 1:
            for i in range(1, len(folds[0])):
                Label(self.list, text=folds[0][i], font=('Arial', 8), bg="White").grid(row=i, column=3, pady=5, padx=15)
                Label(self.list, text=folds[1][i], font=('Arial', 5), bg="White").grid(row=i, column=4, pady=5, padx=2)
                Button(self.list, text='Delete', font=('Arial', 10), bg="Red", fg="White",
                            command=lambda a=i: self.delFolder(folds[0][a])).grid(row=i, column=5, pady=5, padx=2)

    def addFolder(self, name, path):
        try:
            files.addFolder(name, path)
            messagebox.showinfo('Succeed', 'Folder added to musics folders list.')
            self.musicFrame.destroy()
            self.musicsFolder()
            app.putScreen(self.screen)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to add the folder. Error:\n{e}')

    def findFolder(self):
        self.local.delete(0, END)
        self.local.insert(0, filedialog.askdirectory())
        app.putScreen(self.screen)

    def delFolder(self, name):
        try:
            if messagebox.askyesno('Delete', 'Do you want to delete this folder from the folders list?'):
                files.delFolder(name)
                messagebox.showinfo('Succeed', 'Folder deleted from the musics folders list.')
                self.musicFrame.destroy()
                self.musicsFolder()
                app.putScreen(self.screen)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to delete the folder. Error: \n{e}')

def main(): # Main function
    global app, root

    root = Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    print('Running...')
    main()
