from pytube import YouTube
import pyautogui as auto
import time, shutil, os
from os import listdir

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