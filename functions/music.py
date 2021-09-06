# Pygame

import pygame.mixer as mixer # Just Importing the mixer module of pygame, instead of the full module

# Benefits: Easy to code, big community, great mixer controls and good sound
# Problems: Bugs when the computer is overasked

def playMusic(PATH):
    musicPlace = PATH

    mixer.init()
    mixer.music.load(musicPlace)
    mixer.music.play(loops=0)
