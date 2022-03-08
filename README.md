# Music Player <img align=center width=40 height=40 src="https://static.wikia.nocookie.net/logopedia/images/c/cb/Apple_Music_Icon_RGB_lg_073120.svg/revision/latest/scale-to-width-down/250?cb=20200921150442" alt="App Icon">

That's my music player, that I created to improve my python skills and some others things. So it's basically a music player, that I'm gonna use in my daily routine, the most advanced things that it has are:
- Playlists creation
- Search Bar
- Random mode
- Music time bar

Observation: While I was using the older version, I had some problems, like very slow in .exe, music bugging, etc. So I started the V2 (starting in the 1.1.0 version)

### Objectives
- Easy to use
- Fast (just a few libs)

### Future Goals <img align=center width=30 height=30 src="https://user-images.githubusercontent.com/62257920/157306127-9342c871-a1cd-43aa-bc80-48f1834e0871.png" alt="Goal">
- .exe version
- Create own icon
- Save data on using (to use AI)
- Download Musics
- Online playing (like discord bots)
- Get others apps playlists and save to use it

### You need to use:
- Install VLC of 32 bits and 64 bits for your pc
- pip install python-vlc pandas pillow (by python)

## LOG

### 1.6.2v (EXE)
- .exe created (using venv and pyinstaller)
- .gitignore update

### 1.6.1v (Ready-to-use update)
- .gitignore template
- Fix played songs background error
- Examples songs
- Restarted databases files (for new users)

### 1.6v (Revolution update)
- Name changed
- ReadME big update

### 1.5.2v (W10 update)
- DLL fix for VLC

### 1.5.1v (Misc update)
- Put commentaries in all the code
- Restarted the databases and the musics folder, to anyone use it in its way
- Fixed an small error of search, when there's no musics
- Fixed error of no playlists found

### 1.5v (Search bar)
- Search by name in All musics

![teste](https://user-images.githubusercontent.com/62257920/140831905-5e36f506-12e8-483b-a73b-4c43fe812adc.png)

### 1.4.3v (General Configuration)
- Basic General configuration (volume, restaure, apply)
- Style of configuration screen
- Deleted Playlists photos option (not much pretty)

### 1.4.2v (Minor upgrades)
- Restart Button
- Upgrade into delete music Folder feature (yes or no)
- Upgrade into create music Folder feature (select folder)
- Put the window in the screen after a function (creation, delete of music folders)
- Music name in the rename pre put in Entry

### 1.4.1v (Folders)
- Full Folders configuration
- "Pre loaded" information

### 1.4v (Basic Configuration)
- Basic configuration screen
- Small upgrades in the Menu
- Border in the player

### 1.3.2v (Unlimited playlists)
- "Scroll" to playlists in the menu
- Symbols in the up and down buttons

### 1.3.1v (Playlist colors)
- Playlist colors when selected

### 1.3v (Music Time bar)
![image](https://user-images.githubusercontent.com/62257920/134737213-5f40ec6e-5022-4dd5-9718-eaf2997be5cd.png)
- Music time position bar
- Improved scales of volume and time bar
- Fixed error of trying to change volume
- Convertor of seconds to '00:00' format

### 1.2.2v (Edit Musics)
Created an way to rename musics or delete them.

### 1.2.1v (Edit Playlists)
Created an way to edit created playlists.

### 1.2v (Basic Application)
![image](https://user-images.githubusercontent.com/62257920/133005711-2b63c00d-448d-4588-908d-58666163d896.png)

I created:
- The player frame (audio functions), menu frame (playlists) and stuff frame (music list)
- Advance and before musics
- Randomize method (perfect working, and tested)
- Keyboard Functions
- Menu Frame (all, recent, playlists)
- Changed the music module, (tkinter -> VLC) Because of the size of tkinter, is much bigger than VLC module, and VLC don't bugs in my pc, like Tkinter.
- Playlists settings (delete and create)

### 1.1.1v (Audio Functions, create all the audio functions that I will use, and test it)
Created the function to play/unpause, pause and check if the music is playing.

### 1.1.0v (Finding the better way to play musics)
I selected Pygame.mixer, because of the big community and the great mixer controls.

### 1.0.0v (Older Version)
