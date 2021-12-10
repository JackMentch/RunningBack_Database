import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import re
import random

conn = sqlite3.connect('football.db')
cur = conn.cursor()

total_receptions = str([f'Week_{i}_Receptions +' for i in range(12,14)])[1:-3].replace("'","").replace(",","")

cur.execute(f"SELECT NAME, {total_receptions} FROM RUNNINGBACK WHERE {total_receptions} > 8 ORDER BY {total_receptions}")
rows = cur.fetchall()

print(rows)


color = (0, 0, 0)

for row in rows:


    name = re.sub(r"([A-Z])", r" \1", row[0]).split()
    name = name[0][0] + " " + name[1]
    if name == "D Andre":
        name = "D Swift"

    if name == "A J":
        name = "AJ Dillon"

    if name == "J D":
        name = "JD McKis."

    plt.bar(name, row[1])

    plt.annotate(str(row[1]),  # this is the text
                 (name, row[1]),  # these are the coordinates to position the label
                 textcoords="offset points",  # how to position the text
                 size=18,
                 color=color,
                 xytext=(0, 5),  # distance from text to points (x,y)
                 ha='center')

    plt.annotate(name,  # this is the text
                 (name, row[1]),  # these are the coordinates to position the label
                 textcoords="data",  # how to position the text
                 size=20,
                 rotation=90,
                 color=color,
                 xytext=(name, 2),  # distance from text to points (x,y)
                 ha='center')

    print(row)

plt.xticks(fontsize=14, rotation=90, color=(1,1,1))
plt.ylabel('Receptions', size=15)
plt.title('RB Receptions for Weeks 11-13')
plt.text(0,80,'Minimum 350 Snaps')
plt.show()