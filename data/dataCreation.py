import sqlite3

con = sqlite3.connect('./data/data.sqlite')
cur = con.cursor()

# Playlists
#cur.execute('DROP TABLE IF EXISTS Playlists')
#cur.execute('CREATE TABLE Playlists (Name TEXT, Musics TEXT)') # Musics will have a ; to separate

con.close()
