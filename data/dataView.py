import sqlite3
import pandas as pd

con = sqlite3.connect('./data/data.sqlite')
cur = con.cursor()

df = pd.read_sql_query("SELECT * from Playlists", con)
#df = pd.read_sql_query("SELECT * from Folders", con)
#df = pd.read_sql_query("SELECT * from Volume", con)

print(df)

cur.close()
