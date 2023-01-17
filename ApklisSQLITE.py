import sqlite3
import pandas as pd

connection=sqlite3.connect("Apklis/Apklis.db")
cursor=connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Comments (AppName TEXT PRIMARY KEY, Comments TEXT NOT NULL, Num TEXT,  Score TEXT, LastUpdate TEXT, Version TEXT)")
         
#cursor.execute("INSERT OR REPLACE INTO Comments (Name, Comments, Num) VALUES (?, ?, ?)", (str(link),str(List_of_rows), str(Number(link))))   

#cursor.execute("drop table Comments")
#connection.commit()  



cursor.execute("SELECT Comments FROM Comments")   
Total=cursor.fetchall()
dframe=pd.DataFrame(Total)
newFrame=dframe.pop(0)
newFrame.to_csv('emoyiGood.csv', index=False)

 

#sqlite3 -header -csv C:\Frank\pyNew\Picta\Picta.db "select Links,Num,Category from Comments;" >Picta.csv 