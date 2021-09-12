from os import listdir

def findMusics(playlist=""):
    musics = []
    if not playlist:
        for m in listdir('./musics/'):
            musics.append(m[:-4]) # Take off extension (.mp4)

    musics.sort(key=lambda v: v.upper())

    return musics
