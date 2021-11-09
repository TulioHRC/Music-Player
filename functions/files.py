import os
import sqlite3
import pandas as pd

# Folders part

def readFolders():
    con = sqlite3.connect("./data/data.sqlite")
    cur = con.cursor()

    df = pd.read_sql_query("SELECT * FROM Folders", con)

    cur.close()

    return [df["Name"].values, df["Path"].values]

def addFolder(name, path):
    con = sqlite3.connect("./data/data.sqlite")
    cur = con.cursor()

    cur.execute('INSERT INTO Folders (Name, Path) VALUES (?, ?)', (name, path))
    con.commit()

    cur.close()

def delFolder(name):
    con = sqlite3.connect("./data/data.sqlite")
    cur = con.cursor()

    sql = """DELETE FROM Folders WHERE Name = ?"""

    cur.execute(sql, (name,))
    con.commit()

    cur.close()

# Default Volume Part

def readVolume():
    con = sqlite3.connect('./data/data.sqlite')
    cur = con.cursor()

    df = pd.read_sql_query('SELECT * FROM Volume', con)

    cur.close()

    return df['Value'].values[0]

def saveVolume(value):
    con = sqlite3.connect("./data/data.sqlite")
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS Volume')
    cur.execute('CREATE TABLE Volume (Value TEXT)')
    cur.execute('INSERT INTO Volume (Value) VALUES (?)', (str(value),))
    con.commit()

    cur.close()

# Pre Load Part

def preLoad
    folders = readFolders()
    volume = int(readVolume())

    musics = set()

    for folder in folders[1]:
        for m in os.listdir(folder):
            if m.split('.')[-1] == 'mp3': # Only accept .mp3
                musics.add(m[:-4]) # Take off extension (.mp3)

    return [list(musics), folders, volume]

# Musics part

def findMusics(playlist="", order="char", preData=''):
    folders = preData[1][1]

    musics = set()

    if not playlist:
        if preData: # "Pre-Load" mode
            musics = preData[0]
        else:
            for folder in folders:
                for m in os.listdir(folder):
                    if m.split('.')[-1] == 'mp3': # Only accept .mp3
                        musics.add(m[:-4]) # Take off extension (.mp3)
    else:
        musics = playlist.split(';')

    musics = list(musics)

    if order == "char":
        musics.sort(key=lambda v: v.upper())
    elif order == "date":
        musics.sort(key=lambda x: os.path.getmtime(f"{getRealPath(x, list(folders))}\\{x}.mp3"))
        musics.reverse()

    return musics

def getRealPath(name, folders=''): # Get real music path
    if isinstance(folders, str): folders = readFolders()[1]
    res = './musics/'
    for folder in folders:
        if f'{name}.mp3' in os.listdir(folder):
            res = folder
    return str(res)

def renameMusic(path, new):
    os.rename(f"{getRealPath(path)}\\{path}.mp3", f"{getRealPath(path)}\\{new}.mp3")

def deleteMusic(path):
    os.remove(f"{getRealPath(path)}\\{path}.mp3")
