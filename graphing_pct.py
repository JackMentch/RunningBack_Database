import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import re
import random

conn = sqlite3.connect('football.db')
cur = conn.cursor()

total_snaps = str([f'Week_{i}_Snaps +' for i in range(11,13)])[1:-3].replace("'","").replace(",","")

cur.execute(f"SELECT NAME, SNAP_PCT FROM RUNNINGBACK WHERE SNAP_PCT > 30 and TOTAL_SNAPS > 350 ORDER BY SNAP_PCT")
rows = cur.fetchall()

print(rows)


color = (0, 0, 0)

for row in rows:


    name = re.sub(r"([A-Z])", r" \1", row[0]).split()
    name = name[0][0] + " " + name[1]
    if name == "D Andre":
        name = "D Swift"

    plt.bar(name, row[1])

    plt.annotate(str(row[1])+"%",  # this is the text
                 (name, row[1]),  # these are the coordinates to position the label
                 textcoords="offset points",  # how to position the text
                 size=12,
                 color=color,
                 xytext=(0, 5),  # distance from text to points (x,y)
                 ha='center')

    print(row)

plt.ylabel('Snap %', size=15)
plt.title('RB Season Snap % in Games Active')
plt.text(0,80,'Minimum 350 Snaps')
plt.show()