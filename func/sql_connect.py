import sqlite3
import os


def sql_connect(db_name):
    db_path = os.path.join('database', f'{db_name}.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", (db_name, ))
    if cursor.fetchone()[0] == 1:
        cursor.execute(f"SELECT * FROM {db_name}")
        table = cursor.fetchall()
    else:
        table = []
        # print('No such table.')
    conn.commit()
    conn.close()
    return table