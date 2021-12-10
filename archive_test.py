import sqlite3
import matplotlib.pyplot as plt
import re

conn = sqlite3.connect('football.db')
cur = conn.cursor()


for row in cur.execute("PRAGMA table_info('RUNNINGBACK')").fetchall():
    print(row)


total_receptions = str([f'Week_{i}_Receptions +' for i in range(1,13)])[1:-3].replace("'","").replace(",","")
total_carries = str([f'Week_{i}_Carries +' for i in range(1,13)])[1:-3].replace("'","").replace(",","")


print("-----------------------------------")


cur.execute(f"SELECT NAME, Week_12_Receptions, Week_12_Carries FROM RUNNINGBACK WHERE Week_12_Receptions > 4 and Week_12_Carries > 19")

rows = cur.fetchall()

for row in rows:
    print(row)

print("-----------------------------------")

stat = str([f'Week_{i}_Carries' for i in range(1,15)])[1:-1].replace("'","")
cur.execute(f"SELECT NAME, {stat}, TOTAL_Carries FROM RUNNINGBACK WHERE NAME = 'AJDillon' or NAME = 'AaronJones'")

rows = cur.fetchall()

for row in rows:
    print(row)
    name = re.sub(r"([A-Z])", r" \1", row[0]).split()
    name = name[0] +" "+ name[1]
    weeks = [i for i in range(1,15)]
    data = list(row[1:15])

    counter = 0
    for week in [i for i, value in enumerate(data) if value == 0]:
        print(week)
        weeks.pop(week - counter)
        data.pop(week  - counter)
        counter += 1


    xy = zip(weeks, data)

    if name == "Aaron Jones":
        plt.plot(weeks, data, 'go-', label="Aaron Jones")
    else:
        plt.plot(weeks, data, 'ro-', label="AJ Dillon")

    for point in xy:
        plt.annotate(point[1],  # this is the text
                     (point[0],point[1]),  # these are the coordinates to position the label
                     textcoords="offset points",  # how to position the text
                     xytext=(-2, 8),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center

plt.ylabel('Rushing Attempts', size=12)
plt.xlabel('Week', size=12)
plt.title(f'Aaron Jones vs AJ Dillon Rushing Attempts per Game')
plt.legend(loc='upper left')

plt.show()



#
#
# cur.execute(f"SELECT NAME, RUSHING_TOUCHDOWNS, AVG_CARRIES FROM RUNNINGBACK WHERE RUSHING_TOUCHDOWNS > 4")
# rows = cur.fetchall()
#
# print(rows)
#
#
#
#
# for row in rows:
#     r = random.random()
#     b = random.random()
#     g = random.random()
#     color = (r, g, b)
#
#     plt.plot(row[1], row[2])
#
#     name = re.sub(r"([A-Z])", r" \1", row[0]).split()
#
#
#     plt.annotate(name[0][0]+" "+name[1],  # this is the text
#                  (row[1], row[2]),  # these are the coordinates to position the label
#                  textcoords="offset points",  # how to position the text
#                  size=15,
#                  color=color,
#                  xytext=(0, 0),  # distance from text to points (x,y)
#                  ha='center')
#
#     print(row)
#
# plt.xlim((4,15))
# plt.ylabel('Avg. Carries per Game', size=15)
# plt.xlabel('Rushing Touchdowns', size=15)
# plt.title('Avg Carries vs Rushing TDs')
# plt.show()
