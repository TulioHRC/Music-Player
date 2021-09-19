# VLC

import vlc

# Don't bugs in my PC

def playMusic(PATH, unpause, firstTime=0):
    global music

    if unpause == 1:
        music.play()
    else:
        if not firstTime:
            music.stop() # "Kills" the last song
        music = vlc.MediaPlayer(PATH)
        music.play()

def pauseMusic():
    music.pause()

def checkMusic():
    return music.is_playing()

def volume(value):
    try:
        music.audio_set_volume(int(value))
    except Exception as e:
        print('Volume is trying to change, before the mixer is initialized.')
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
