import sqlite3
import matplotlib.pyplot as plt
import re


conn = sqlite3.connect('football.db')
cur = conn.cursor()

total_snaps = str([f'Week_{i}_Snaps +' for i in range(13,14)])[1:-3].replace("'","").replace(",","")

cur.execute(f"SELECT NAME, {total_snaps} FROM RUNNINGBACK WHERE {total_snaps} > 40 ORDER BY {total_snaps}")
rows = cur.fetchall()

print(rows)


color = (0, 0, 0)

for row in rows:


    name = re.sub(r"([A-Z])", r" \1", row[0]).split()
    name = name[0][0] + " " + name[1]
    if name == "A J":
        name = "AJ Dillon"

    plt.bar(name, row[1])

    plt.annotate(row[1],  # this is the text
                 (name, row[1]),  # these are the coordinates to position the label
                 textcoords="offset points",  # how to position the text
                 size=12,
                 color=color,
                 xytext=(0, 5),  # distance from text to points (x,y)
                 ha='center')

    plt.annotate(name,  # this is the text
                 (name, row[1]),  # these are the coordinates to position the label
                 textcoords="data",  # how to position the text
                 size=20,
                 rotation=90,
                 color=color,
                 xytext=(name, 5),  # distance from text to points (x,y)
                 ha='center')

    print(row)

plt.xticks(fontsize=14, rotation=90, color=(1,1,1))
plt.ylabel('Total Snaps', size=15)
plt.title('RB Total Snaps for Week 13')
plt.show()