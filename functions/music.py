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
