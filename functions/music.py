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
