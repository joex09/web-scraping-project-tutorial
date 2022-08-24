import pandas as pd
import requests 
import sqlite3
from bs4 import BeautifulSoup

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data,"html.parser")
tablas = soup.findAll("table")

for i, tabla in enumerate(tablas):
    if ("Tesla Quarterly Revenue" in str(tabla)): 
        rev = i 

df = pd.DataFrame(columns=["date","revenue"])


for fila in tablas[rev].tbody.find_all("tr"):
    datos= fila.find_all("td")


for fila in tablas[rev].tbody.find_all("tr"):
    datos= fila.find_all("td")
    if len(datos)>0:
        fecha=datos[0].text
        revenue=datos[1].text.replace("$","").replace(",","")
        df = df.append({"date":fecha,"revenue":revenue},ignore_index=True)

df=df[df["revenue"]!=""]

records = df.to_records(index=False)
list_of_tuples = list(records)

connection = sqlite3.connect('Tesla.db')
c = connection.cursor()

# Create table
c.execute('''CREATE TABLE revenue
             (Date, Revenue)''')


# Insert the values
c.executemany('INSERT INTO revenue VALUES (?,?)', list_of_tuples)

# Save (commit) the changes
connection.commit()

for row in c.execute('SELECT * FROM revenue'):
    print(row)
