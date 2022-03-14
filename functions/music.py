# Pygame

from pygame import mixer
from mutagen.mp3 import MP3

def playMusic(PATH, unpause, firstTime=0):
    global music

    if unpause == 1:
        mixer.music.unpause()
    else:
        if not firstTime:
            mixer.music.stop()

        music = PATH

        mixer.init()
        mixer.music.load(PATH)
        mixer.music.play()

def changeMusicPosition(newTime):
    pauseMusic()
    mixer.music.set_pos(int(newTime))
    mixer.music.unpause()

def pauseMusic():
    mixer.music.pause()

def checkMusic():
    return mixer.music.get_busy()

def getTimes(audioFile, change):
    audio = MP3(audioFile)
    return [int(round(mixer.music.get_pos()/1000, 0)) + int(round(change, 0)), int(audio.info.length)]

def volume(value):
    if 'music' in globals(): # Check if the global variable exists
        try:
            mixer.music.set_volume(int(value)/100) # 0.0 - 1.0
        except Exception as e:
            print(e)

"""
# VLC

from vlc import MediaPlayer

# Don't bugs in my PC

def playMusic(PATH, unpause, firstTime=0):
    global music

    if unpause == 1:
        music.play()
    else:
        if not firstTime:
            music.stop() # "Kills" the last song
        music = MediaPlayer(PATH)
        music.play()

def changeMusicPosition(newTime):
    music.set_time(int(newTime))

def pauseMusic():
    music.pause()

def checkMusic():
    return music.is_playing()

def getTimes():
    return [int(round(music.get_time()/1000, 0)), int(round(music.get_length()/1000, 0))]

def volume(value):
    if 'music' in globals(): # Check if the global variable exists
        try:
            music.audio_set_volume(int(value))
        except Exception as e:
            print(e)
"""
