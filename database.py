import sqlite3
#
conn = sqlite3.connect('football.db')
cur = conn.cursor()


cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

cur.execute("DROP TABLE RUNNINGBACK")

touches = [f"Week_{i}_Touches" for i in range(1,18)]
carries = [f"Week_{i}_Carries" for i in range(1,18)]
receptions = [f"Week_{i}_Receptions" for i in range(1,18)]
snaps = [f"Week_{i}_Snaps" for i in range(1,18)]
targets = [f"Week_{i}_Targets" for i in range(1,18)]
redzone_targets = [f"Week_{i}_RZ_Targets" for i in range(1,18)]
redzone_receptions = [f"Week_{i}_RZ_Receptions" for i in range(1,18)]
redzone_touches = [f"Week_{i}_RZ_Touches" for i in range(1,18)]
redzone_carries = [f"Week_{i}_RZ_Carries" for i in range(1,18)]

database_columns = [touches, carries, receptions, snaps, targets,
                    redzone_targets, redzone_receptions, redzone_touches,
                    redzone_carries]


conn.execute(f'''CREATE TABLE RUNNINGBACK
         (NAME TEXT PRIMARY KEY     NOT NULL,
        
        AVG_TOUCHES           REAL,
        TOTAL_TOUCHES           INT,
        
        AVG_RECEPTIONS           REAL,
        TOTAL_RECEPTIONS           INT,
        RECEIVING_TOUCHDOWNS           INT,
        
        AVG_CARRIES           REAL,
        TOTAL_CARRIES           INT,
        CARRIES_PCT           REAL,
        RUSHING_TOUCHDOWNS           INT,
        
        AVG_SNAPS           REAL,
        TOTAL_SNAPS          INT,
        SNAP_PCT           REAL,
        
        AVG_TARGETS          REAL,
        TOTAL_TARGETS          INT,
        TARGET_PCT           REAL,
        CATCH_PCT           REAL,
        
        AVG_RZ_CARRIES          REAL,
        TOTAL_RZ_CARRIES         INT,
        
        AVG_RZ_TOUCHES          REAL,
        TOTAL_RZ_TOUCHES         INT,
        
        AVG_RZ_TARGETS          REAL,
        TOTAL_RZ_TARGETS         INT,
        
        AVG_RZ_RECEPTIONS          REAL,
        TOTAL_RZ_RECEPTIONS         INT,
        
        TOTAL_TOUCHDOWNS           INT      
         );''')

for column_values in database_columns:
    for column in column_values:
        conn.execute('''ALTER TABLE RUNNINGBACK ADD COLUMN ''' + column + ''' INTEGER''')


for row in cur.execute("PRAGMA table_info('RUNNINGBACK')").fetchall():
    print(row)


conn.close()