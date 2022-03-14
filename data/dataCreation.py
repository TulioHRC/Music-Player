import sqlite3

con = sqlite3.connect('./data/data.sqlite')
cur = con.cursor()

# Playlists
cur.execute('DROP TABLE IF EXISTS Playlists')
cur.execute('CREATE TABLE Playlists (Name TEXT, Musics TEXT)') # Musics will have a ; to separate

# Music Folders
cur.execute('DROP TABLE IF EXISTS Folders')
cur.execute('CREATE TABLE Folders (Name TEXT, Path TEXT)')
cur.execute('INSERT INTO Folders (Name, Path) VALUES (?, ?)', ('Default', 'musics/'))
con.commit()

# Default Volume
cur.execute('DROP TABLE IF EXISTS Volume')
cur.execute('CREATE TABLE Volume (Value TEXT)')
cur.execute('INSERT INTO Volume (Value) VALUES (?)', ('50',))
con.commit()

con.close()
