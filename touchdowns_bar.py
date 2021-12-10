import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import re
import pandas as pd

conn = sqlite3.connect('football.db')
cur = conn.cursor()

total_snaps = str([f'Week_{i}_Snaps +' for i in range(11,13)])[1:-3].replace("'","").replace(",","")

df = pd.read_sql_query(f"SELECT NAME, RUSHING_TOUCHDOWNS, RECEIVING_TOUCHDOWNS FROM RUNNINGBACK WHERE TOTAL_TOUCHDOWNS > 6 ORDER BY TOTAL_TOUCHDOWNS", conn)
df = df.set_index('NAME')


ax = df.plot.bar(rot=0)

plt.show()
# x = np.arange(len(rows))  # the label locations
# width = 0.35  # the width of the bars
# fig, ax = plt.subplots()
#
# names = []
#
# color = (0, 0, 0)
#
# for row in rows:
#
#
#     name = re.sub(r"([A-Z])", r" \1", row[0]).split()
#     name = name[0][0] + " " + name[1]
#     if name == "D Andre":
#         name = "D Swift"
#
#     names.append(name)
#
#     rects1 = ax.bar(x - width/2, row[1], width)
#     rects2 = ax.bar(x + width/2, row[2], width)
#
# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
# ax.set_xticks(x, names)
# ax.legend()
#
# ax.bar_label(rects1, padding=3)
# ax.bar_label(rects2, padding=3)
#
# fig.tight_layout()
#
# plt.show()