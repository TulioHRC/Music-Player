import os

def findMusics(playlist="", order="char"):
    musics = []
    if not playlist:
        for m in os.listdir('./musics/'):
            musics.append(m[:-4]) # Take off extension (.mp4)
    else:
        musics = playlist.split(';')

    if order == "char":
        musics.sort(key=lambda v: v.upper())
    elif order == "date":
        musics.sort(key=lambda x: os.path.getmtime(f"./musics/{x}.mp3"))
        musics.reverse()

    return musics
