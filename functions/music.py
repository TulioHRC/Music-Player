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
# Pygame

import pygame.mixer as mixer # Just Importing the mixer module of pygame, instead of the full module

# Benefits: Easy to code, big community, great mixer controls and good sound
# Problems: Bugs when the computer is overasked

def playMusic(PATH, unpause):
    if unpause == 1:
        mixer.music.unpause()
    else:
        mixer.init()
        mixer.music.load(PATH)
        mixer.music.play(loops=0)

def pauseMusic():
    mixer.music.pause()

def checkMusic():
    return mixer.music.get_busy()

def volume(value):
    try:
        mixer.music.set_volume(int(value)/100)
    except:
        print('Volume is trying to change, before the mixer is initialized.')
"""
