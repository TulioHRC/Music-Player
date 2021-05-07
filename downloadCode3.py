from pytube import YouTube
import pyautogui as auto
import os
import shutil
import time
	
def download(URL):
	try:
		yt = YouTube(str(URL))
		  
		video = yt.streams.filter().first()
		out_file = video.download()
		
		import moviepy.editor

		video1 = moviepy.editor.VideoFileClip(os.path.join(out_file))
		video1.audio.write_audiofile(os.path.join(out_file[:-3] + "mp3"))

		video1.close()

		shutil.move(out_file[:-3] + "mp3", path)
		
		os.remove(out_file)

		print(yt.title + " has been successfully downloaded.")
	except Exception as e:
		print(e)
		auto.alert("There was an error on the app.")

def search(name):
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys 
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC

	PATH = r'C:\Program Files (x86)\WebDrivers\chromedriver.exe' # Testar com chromedriver na mesma pasta
	driver = webdriver.Chrome(PATH)

	driver.get("https://youtube.com") # abri a url dada

	search = driver.find_element_by_id("search")
	time.sleep(1)
	search.send_keys(name)
	time.sleep(1)
	search.send_keys(Keys.RETURN)

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
		download(search(vid))

	auto.alert("The videos have been downloaded, now you can use your PC.")