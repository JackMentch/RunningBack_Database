
from modules.touches_runningbacks import get_touches_runningbacks
from modules.receiving_runningbacks import get_receiving_runningbacks
from modules.carries_runningbacks import get_carries_runningbacks
from modules.snaps_runningbacks import get_snaps_runningbacks
from modules.targets_runningbacks import get_targets_runningbacks
from modules.rz_carries_runningbacks import get_rz_carries_runningbacks
from modules.rz_touches_runningbacks import get_rz_touches_runningbacks
from modules.rz_targets_runningbacks import get_rz_targets_runningbacks
from modules.rz_receptions_runningbacks import get_rz_receptions_runningbacks
import time
import pandas as pd
import sqlite3
import re

regex = re.compile('[^a-zA-Z]')

start = time.time()

# ____TOUCHES STATS____
# https://www.lineups.com/nfl/player-stats/running-back-rb-touches
# (1, 'AVG_TOUCHES', 'INT', 1, None, 0)
# (2, 'TOTAL_TOUCHES', 'INT', 1, None, 0)
# (25, 'TOTAL_TOUCHDOWNS', 'INT', 1, None, 0)
# (26 - 42, 'Week_i_Touches', 'INTEGER', 1, None, 0)

touches_stats = get_touches_runningbacks()
# print(touches_stats)

# ____RECEPTIONS STATS____
# https://www.lineups.com/nfl-receptions/running-back-rb
# (3, 'AVG_RECEPTIONS', 'INT', 1, None, 0)
# (4, 'TOTAL_RECEPTIONS', 'INT', 1, None, 0)
# (5, 'RECEIVING_TOUCHDOWNS', 'INT', 1, None, 0)
# (60 - 76, 'Week_i_Receptions', 'INTEGER', 1, None, 0)

reception_stats = get_receiving_runningbacks()
# print(reception_stats)

df = pd.merge(touches_stats, reception_stats, on='Name', how='outer')

# ____CARRIES STATS____
# https://www.lineups.com/nfl/player-stats/running-back-rb-rush-attempts
# (6, 'AVG_CARRIES', 'INT', 1, None, 0)
# (7, 'TOTAL_CARRIES', 'INT', 1, None, 0)
# (8, 'CARRIES_PCT', 'REAL', 1, None, 0)
# (9, 'RUSHING_TOUCHDOWNS', 'INT', 1, None, 0)
# (43 - 59, 'Week_i_Carries', 'INTEGER', 1, None, 0)

carries_stats = get_carries_runningbacks()
# print(carries_stats)

df = pd.merge(df, carries_stats, on='Name', how='outer')

# ____SNAPS STATS____
# https://www.lineups.com/nfl/snap-counts/running-back-rb-snap-counts
# (10, 'AVG_SNAPS', 'INT', 1, None, 0)
# (11, 'TOTAL_SNAPS', 'INT', 1, None, 0)
# (12, 'SNAP_PCT', 'REAL', 1, None, 0)
# (77 - 93, 'Week_i_Snaps', 'INTEGER', 1, None, 0)

snaps_stats = get_snaps_runningbacks()
# print(snaps_stats)

df = pd.merge(df, snaps_stats, on='Name', how='outer')

# ____TARGETS STATS____
# https://www.lineups.com/nfl/nfl-targets/running-back-rb-targets
# (13, 'AVG_TARGETS', 'INT', 1, None, 0)
# (14, 'TOTAL_TARGETS', 'INT', 1, None, 0)
# (15, 'TARGET_PCT', 'REAL', 1, None, 0)
# (16, 'CATCH_PCT', 'REAL', 1, None, 0)
# (94 - 110, 'Week_i_Targets', 'INTEGER', 1, None, 0)

targets_stats = get_targets_runningbacks()
# print(targets_stats)

df = pd.merge(df, targets_stats, on='Name', how='outer')

# ____REDZONE CARRIES STATS____
# https://www.lineups.com/nfl/running-back-rb-redzone-rush-attempts
# (17, 'AVG_RZ_CARRIES', 'INT', 1, None, 0)
# (18, 'TOTAL_RZ_CARRIES', 'INT', 1, None, 0)
# (162 - 178, 'Week_i_RZ_Carries', 'INTEGER', 1, None, 0)

rz_carries_stats = get_rz_carries_runningbacks()
# print(rz_carries_stats)

df = pd.merge(df, rz_carries_stats, on='Name', how='outer')

# ____REDZONE TOUCHES STATS____
# https://www.lineups.com/nfl/running-back-rb-redzone-touches
# (19, 'AVG_RZ_TOUCHES', 'INT', 1, None, 0)
# (20, 'TOTAL_RZ_TOUCHES', 'INT', 1, None, 0)
# (145 - 161, 'Week_i_RZ_Touches', 'INTEGER', 1, None, 0)

rz_touches_stats = get_rz_touches_runningbacks()
# print(rz_touches_stats)

df = pd.merge(df, rz_touches_stats, on='Name', how='outer')

# ____REDZONE TARGETS STATS____
# https://www.lineups.com/nfl/running-back-rb-redzone-targets
# (21, 'AVG_RZ_TARGETS', 'INT', 1, None, 0)
# (22, 'TOTAL_RZ_TARGETS', 'INT', 1, None, 0)
# (111 - 127, 'Week_i_RZ_Targets', 'INTEGER', 1, None, 0)

rz_targets_stats = get_rz_targets_runningbacks()
# print(rz_targets_stats)

df = pd.merge(df, rz_targets_stats, on='Name', how='outer')

# ____REDZONE RECEPTION STATS____
# https://www.lineups.com/nfl/running-back-rb-redzone-receptions
# (23, 'AVG_RZ_RECEPTIONS', 'INT', 1, None, 0)
# (24, 'TOTAL_RZ_RECEPTIONS', 'INT', 1, None, 0)
# (128 - 144, 'Week_i_RZ_Receptions', 'INTEGER', 1, None, 0)

rz_receptions_stats = get_rz_receptions_runningbacks()
# print(rz_receptions_stats)

df = pd.merge(df, rz_receptions_stats, on='Name', how='outer')

# df.to_csv("database.csv", sep=',')
#
# df = pd.read_csv("database.csv")

df = df.fillna(0)

conn = sqlite3.connect('football.db')
cur = conn.cursor()

for index, row in df.iterrows():
    name = regex.sub('',row['Name'])

    touches = str([f'Week_{i}_Touches' for i in range(1,18)])[1:-1].replace("'","")
    receptions = str([f'Week_{i}_Receptions' for i in range(1,18)])[1:-1].replace("'","")
    carries = str([f'Week_{i}_Carries' for i in range(1,18)])[1:-1].replace("'","")
    snaps = str([f'Week_{i}_Snaps' for i in range(1,18)])[1:-1].replace("'","")
    targets = str([f'Week_{i}_Targets' for i in range(1,18)])[1:-1].replace("'","")
    rz_targets = str([f'Week_{i}_RZ_Targets' for i in range(1,18)])[1:-1].replace("'","")
    rz_receptions = str([f'Week_{i}_RZ_Receptions' for i in range(1,18)])[1:-1].replace("'","")
    rz_carries = str([f'Week_{i}_RZ_Carries' for i in range(1,18)])[1:-1].replace("'","")
    rz_touches = str([f'Week_{i}_RZ_Touches' for i in range(1,18)])[1:-1].replace("'","")

    touches_data = str([row[f'Week_{i}_Touches'] for i in range(1,18)])[1:-1]
    receptions_data = str([row[f'Week_{i}_Receptions'] for i in range(1,18)])[1:-1]
    carries_data = str([row[f'Week_{i}_Carries'] for i in range(1,18)])[1:-1]
    snaps_data = str([row[f'Week_{i}_Snaps'] for i in range(1,18)])[1:-1]
    targets_data = str([row[f'Week_{i}_Targets'] for i in range(1,18)])[1:-1]
    rz_targets_data = str([row[f'Week_{i}_RZ_Targets'] for i in range(1,18)])[1:-1]
    rz_receptions_data = str([row[f'Week_{i}_RZ_Receptions'] for i in range(1,18)])[1:-1]
    rz_carries_data = str([row[f'Week_{i}_RZ_Carries'] for i in range(1,18)])[1:-1]
    rz_touches_data = str([row[f'Week_{i}_RZ_Touches'] for i in range(1,18)])[1:-1]

    sqlite_insert_query = f"""INSERT INTO RUNNINGBACK
                                  (NAME, AVG_TOUCHES, TOTAL_TOUCHES, AVG_RECEPTIONS, TOTAL_RECEPTIONS, RECEIVING_TOUCHDOWNS,
                                  AVG_CARRIES, TOTAL_CARRIES, CARRIES_PCT, RUSHING_TOUCHDOWNS, AVG_SNAPS, TOTAL_SNAPS,
                                  SNAP_PCT, AVG_TARGETS, TOTAL_TARGETS, TARGET_PCT, CATCH_PCT, AVG_RZ_CARRIES, TOTAL_RZ_CARRIES,
                                  AVG_RZ_TOUCHES, TOTAL_RZ_TOUCHES, AVG_RZ_TARGETS, TOTAL_RZ_TARGETS, AVG_RZ_RECEPTIONS,
                                  TOTAL_RZ_RECEPTIONS, TOTAL_TOUCHDOWNS, {touches}, {receptions}, {carries}, {snaps}, {targets},
                                  {rz_targets}, {rz_receptions}, {rz_carries}, {rz_touches})
                                   VALUES
                                  ('{name}',{row['AVG_TOUCHES']},{row['TOTAL_TOUCHES']},{row['AVG_RECEPTIONS']},
                                    {row['TOTAL_RECEPTIONS']}, {row['RECEIVING_TOUCHDOWNS']}, {row['AVG_CARRIES']},
                                    {row['TOTAL_CARRIES']}, {row['CARRIES_PCT']}, {row['RUSHING_TOUCHDOWNS']},
                                    {row['AVG_SNAPS']}, {row['TOTAL_SNAPS']}, {row['SNAP_PCT']},
                                    {row['AVG_TARGETS']}, {row['TOTAL_TARGETS']}, {row['TARGET_PCT']},
                                    {row['CATCH_PCT']}, {row['AVG_RZ_CARRIES']}, {row['TOTAL_RZ_CARRIES']}, {row['AVG_RZ_TOUCHES']},
                                    {row['TOTAL_RZ_TOUCHES']}, {row['AVG_RZ_TARGETS']}, {row['TOTAL_RZ_TARGETS']}, {row['AVG_RZ_RECEPTIONS']},
                                    {row['TOTAL_RZ_RECEPTIONS']}, {row['TOTAL_TOUCHDOWNS']}, {touches_data}, {receptions_data}, {carries_data}, {snaps_data}, {targets_data},
                                    {rz_targets_data}, {rz_receptions_data}, {rz_carries_data}, {rz_touches_data})"""

    count = cur.execute(sqlite_insert_query)

conn.commit()

end = time.time()
print(end-start)
