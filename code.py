from tkinter import *
from tkinter import ttk, messagebox
import os, sys, pygame, html, shutil, time
from os import listdir, startfile
from os.path import isfile, join
from random import randint
import time

SymBack = html.unescape('&#9664;&#9664;')
SymPlay = html.unescape('&#9654;')
SymPause = html.unescape('  &#9612;&#9612;')
SymFow = html.unescape('&#9654;&#9654;')

# Download code functions

from pytube import YouTube
import pyautogui as auto

downloadedM = []

def download(URL, path):
	global downloadedM
	try:
		yt = YouTube(str(URL))
		  
		video = yt.streams.filter().first()
		out_file = video.download()

		if out_file[:-4].split("\\")[-1] in musics():
			os.remove(out_file)
			int("Already exists")
		
		import moviepy.editor

		video1 = moviepy.editor.VideoFileClip(os.path.join(out_file))
		video1.audio.write_audiofile(os.path.join(out_file[:-3] + "mp3"))

		video1.close()

		shutil.move(out_file[:-3] + "mp3", path)
		
		os.remove(out_file)

		downloadedM.append(yt.title)
	except Exception as e:
		print(e)
		auto.alert(f"There was an error on the app. The music url {URL} can't be downloaded!\nError: {e}")

def search(name):
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys 
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC

	PATH = r'chromedriver.exe' # Testar com chromedriver na mesma pasta
	driver = webdriver.Chrome(PATH)

	driver.get("https://youtube.com") # abri a url dada

	search = driver.find_element_by_id("search")
	time.sleep(2)
	search.send_keys(name)
	time.sleep(2)
	return_button = driver.find_element_by_id("search-icon-legacy")
	return_button.click()
	try:
	    first_result = WebDriverWait(driver, 15).until(
	        EC.presence_of_element_located((By.ID, "title-wrapper"))
	    )
	    a = first_result.find_element(By.ID, "video-title")
	    return(a.get_attribute('href'))
	except Exception as e:
		print(e)

def go(videos, path):
	auto.alert("Downloading, please don't interact with the app during the download. But you can use the computer normally.")

	for vid in videos:
		download(search(vid), path)

	auto.alert(f"The videos have been downloaded, now you can use your PC. \nList of musics:{downloadedM}")

# Search Functions

def musics(playlist=''):
	musics = []
	if playlist:
		arq = open(f'./playlists/{playlist}.txt', 'r')
		for music in arq: musics.append(music)
	else:
		for music in listdir(f'./musics/'): musics.append(music[:-4])
	return musics

def playlists():
	playlists = []
	for playlist in listdir('./playlists/'):
		playlists.append(playlist[:-4])
	return playlists

# Classes

class MainApp:
	def __init__(self, master):
		self.master = master
		self.master.title('Music Player')
		self.master.configure(background='gray')
		self.master.iconbitmap('./images/music-logo.ico')

		pygame.mixer.init(48000, -16, 1, 2)

		self.play = self.clicked = 0 
		self.r = IntVar() # random var
		self.r.set(0)
		self.v = 50 # volume var
		self.ps = playlists()
		self.playingMusic = ''

		# Main Constrution
		self.randOrder = Checkbutton(self.master, text="Randomly", variable=self.r, fg='black', bg='gray')
		self.randOrder.grid(row=0, column=0)

		Label(self.master, text="Musics", font="size=42", fg='white', bg='gray').grid(row=0, column=2)

		self.PN = StringVar()
		self.PN.set('All')
		self.Options = OptionMenu(self.master, self.PN, *self.ps, command=self.changeL)
		self.Options.config(fg='white', bg='gray', highlightbackground = "gray", highlightcolor= "gray")
		self.Options.grid(row=0, column=3)

		self.Config = Button(self.master, text="Config", command=PlaylistOptions, fg='white', bg='gray')
		self.Config.grid(row=0, column=4)

		self.m = musics()
		self.box = Listbox(self.master, height=10, width=50, selectmode=SINGLE, font="size=30")
		self.box.grid(row=1, column=0, columnspan=5, padx=25)
		for music in self.m:
			self.box.insert(END, music)
		
		self.aM = Label(self.master, text="-", fg='white', bg='gray')
		self.aM.grid(row=2, column=0)

		self.last = Button(self.master, text=SymBack, command=lambda: self.changeM(-1), fg='white', bg='gray').grid(row=2, column=1)
		self.playB = Button(self.master, text=SymPlay, command=self.start, fg='white', bg='gray')
		self.playB.grid(row=2, column=2)
		self.nextB = Button(self.master, text=SymFow, command=lambda: self.changeM(1), fg='white', bg='gray').grid(row=2, column=3)

		self.scaleV = Scale(self.master, from_=0, to=100, orient=HORIZONTAL, command=self.vol, fg='white', bg='gray', highlightbackground = "gray", highlightcolor= "gray")
		self.scaleV.grid(row=2, column=4)
		self.scaleV.set(self.v)

	def start(self):
		self.add = self.playingMusic = self.box.get(ACTIVE)
		if self.add[-1] == '\n':
			self.add = self.add[:-1]
		self.play = 1
		self.playB["text"] = SymPause
		self.playB["command"] = self.stop
		if (len(self.add)-4) < 20:
			self.aM['text'] = self.add
		else:
			self.aM['text'] = self.add[:20] + '...'
		pygame.mixer.music.load(f"./musics/{self.add}.mp3")
		pygame.mixer.music.play(loops=0)
		self.check()
	
	def resume(self):
		self.play = 1
		self.playB["text"] = SymPause
		self.playB["command"] = self.stop
		pygame.mixer.music.unpause()

	def check(self):
		if pygame.mixer.music.get_busy() == 0 and self.play == 1:
			self.changeM(1)
		if self.play == 1:
			root.after(1000, self.check)

	def stop(self):
		self.play = 0
		pygame.mixer.music.pause()
		self.playB["text"] = SymPlay
		self.playB["command"] = self.resume

	def changeM(self, factor):
		self.add = self.playingMusic
		self.box.selection_clear(0, END)
		self.pos = self.m.index(self.add)
		if self.r.get() == 1:
			factor = randint(self.pos*-1, len(self.m)-1-self.pos)
		if (self.pos + factor) >= 0 and (self.pos + factor) != len(self.m):
			self.pos += factor
		elif (self.pos + factor) == len(self.m):
			self.pos = 0
		self.box.selection_set(self.pos)
		self.box.activate(self.pos)
		self.start()

	def changeL(self, value):
		if value == 'All':
			self.m = musics()
		else:
			self.m = musics(str(value))
		self.box = Listbox(self.master, height=10, width=50, selectmode=SINGLE, font="size=30")
		self.box.grid(row=1, column=0, columnspan=5, padx=25)

		for music in self.m:
			self.box.insert(END, music)

	def vol(self, value):
		self.v = int(value)/100
		pygame.mixer.music.set_volume(self.v)


class PlaylistOptions(MainApp):
	def __init__(self):
		app.stop()

		self.screen = Toplevel()
		self.screen.title('Configuration')
		self.screen.geometry('500x350')
		self.screen.iconbitmap('./images/music-logo.ico')

		self.tabs = ttk.Notebook(self.screen)
		self.tabs.pack(pady=5, padx=0)

		self.cFrame = Frame(self.tabs, width=450, height=400, bg='red')
		self.editFrame = Frame(self.tabs, width=450, height=400, bg='yellow')
		self.delFrame = Frame(self.tabs, width=450, height=400, bg='blue')
		self.downloadF = Frame(self.tabs, width=450, height=400, bg='gray')

		self.cFrame.pack(fill='both', expand=True)
		self.editFrame.pack(fill='both', expand=True)
		self.delFrame.pack(fill='both', expand=True)
		self.downloadF.pack(fill='both', expand=True)

		self.tabs.add(self.cFrame, text="Create")
		self.tabs.add(self.editFrame, text="Edit")
		self.tabs.add(self.delFrame, text="Delete")
		self.tabs.add(self.downloadF, text="Auto Download Musics")

		self.ms = musics()

	# Create Frame
		Label(self.cFrame, text='', bg='red').grid(row=0, column=0)
		self.nameC = Entry(self.cFrame, width=25)
		self.nameC.grid(row=1, column=1, pady=3)

		self.boxC = Listbox(self.cFrame, height=10, width=50, selectmode=MULTIPLE, font="size=30")
		self.boxC.grid(row=2, column=0, columnspan=5, padx=25)
		for music in self.ms:
			self.boxC.insert(END, music)

		Label(self.cFrame, text='', bg='red').grid(row=3, column=0)
		Button(self.cFrame, text="Create", command=lambda: self.create(self.nameC.get(), self.boxC)).grid(row=4, column=1)

	# Edit Frame
		Label(self.editFrame, text='', bg='yellow').grid(row=0, column=0)
		
		# Playlist options
		self.plays = playlists()
		self.plays.remove('All')
		self.playlistToEdit = StringVar()
		self.OptionsE = OptionMenu(self.editFrame, self.playlistToEdit, *self.plays, command=self.choose)
		self.OptionsE.grid(row=0, column=3)

		self.boxE = Listbox(self.editFrame, height=10, width=50, selectmode=MULTIPLE, font="size=30")
		self.boxE.grid(row=2, column=0, columnspan=5, padx=25)
		for music in self.ms:
			self.boxE.insert(END, music)

		Label(self.editFrame, text='', bg='yellow').grid(row=3, column=0)
		Button(self.editFrame, text="Edit", command=lambda: self.create(self.playlistToEdit.get(), self.boxE)).grid(row=4, column=1)

	# Delete Frame
		Label(self.delFrame, text='', bg='blue').grid(row=0, column=0)
		self.playName = StringVar()
		self.playName.set('All')
		self.playOptions = OptionMenu(self.delFrame, self.playName, *(playlists()))
		self.playOptions.grid(row=1, column=2)
		Button(self.delFrame, text='Delete', command=self.delete).grid(row=2, column=3)

	# Download frame
		Label(self.downloadF, text='', bg='gray').grid(row=0, column=0)
		Label(self.downloadF, text="Auto Download musics.", bg="#B3B3B3", fg="white").grid(row=1, column=1)

		Label(self.downloadF, text="Name of the music: ", bg="#B3B3B3", fg="white").grid(row=3, column=0, padx=5)
		self.name = Entry(self.downloadF, width=50)
		self.name.grid(row=3, column=1, columnspan=2, padx=2, pady=2)

		Button(self.downloadF, text="Add", command=self.addM).grid(row=3, column=4)

		self.videos = []
		self.boxD = Listbox(self.downloadF, height=10, width=25, selectmode=MULTIPLE, font="size=30")
		self.boxD.grid(row=4, column=0, columnspan=2, padx=25, pady=5)

		Button(self.downloadF, text="Download", command=self.startDown).grid(row=4, column = 4)
		

	def create(self, name, box):
		self.arqold = open(f'playlists/{name}.txt', 'w')
		self.arqold.write('')
		self.arqold.close()
		self.arq = open(f'playlists/{name}.txt', 'a')
		try:
			for pos in box.curselection():
				self.arq.write(self.ms[pos]+'\n')
		except Exception as e:
			print(e)
			messagebox.showerror("Error", f"Ocorred in {pos} of the all playlist to insert in the new playlist.\n Try again.")
			self.screen.destroy()
		self.arq.close()
		app.__init__(app.master)
		self.screen.destroy()

	def choose(self, value):
		self.mToEdit = musics(str(value))
		self.boxE.selection_clear(0, END)
		for music in self.mToEdit:
			self.pos = app.m.index(music[:-1])
			self.boxE.selection_set(self.pos)
			self.boxE.activate(self.pos)
		

	def delete(self):
		os.remove(f'./playlists/{self.playName.get()}.txt')
		app.__init__(app.master)
		self.screen.destroy()

	def addM(self):
		music = self.name.get()
		self.boxD.insert(END, music)
		self.videos.append(music)
		self.name.delete(0, 'end')

	def startDown(self):
		go(self.videos, r".\musics")
		self.screen.destroy()
		app.master.destroy()
		startfile(sys.argv[0])


def main(): 
	global app, root

	root = Tk()
	app = MainApp(root)
	root.mainloop()

if __name__ == '__main__':
    main()