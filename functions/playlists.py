import sqlite3
import pandas as pd

def createPlaylist(name, musicsList):
    musics = ';'.join(musicsList)

    con = sqlite3.connect("./data/data.sqlite")
    cur = con.cursor()

    cur.execute('INSERT INTO Playlists (Name, Musics) VALUES (?, ?)', (name, musics))
    con.commit()

    cur.close()

def deletePlaylist(name):
    con = sqlite3.connect('./data/data.sqlite')
    cur = con.cursor()
    sql = '''DELETE FROM Playlists WHERE Name = ?'''

    cur.execute(sql, (name,))
    con.commit()

    cur.close()


def loadPlaylists():
    con = sqlite3.connect('./data/data.sqlite')
    cur = con.cursor()
    df = pd.read_sql_query("SELECT * FROM Playlists", con)
    cur.close()

    return [df["Name"].values, df["Musics"].values]
