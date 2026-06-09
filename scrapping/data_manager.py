import sqlite3
import datetime


def data_manager(data):
    # Connection
    conn = sqlite3.connect("../monitor/db.sqlite3")
    # Cursor
    cursor = conn.cursor()

    if list(data.keys()):
        store = list(data.keys())[0]
        res = add_store(store, cursor)
        if res:
            env = list(data[store].keys())
            enviroments = (env, res[0])
            res = add_enviroments(enviroments, cursor)
            if res:
                for x in range(len(res)):
                    values = (data[store][enviroments[0][x]], res[x])
                    add_env_values(values, cursor)
                conn.commit()
                print(f"{store}: OK!")


def add_store(data, cursor):
    cursor.execute("""INSERT INTO core_teststore (name)
                   VALUES (?)""", (data,))
    
    cursor.execute("""SELECT id FROM core_teststore
                   WHERE name = ?""", (data,))
    id = cursor.fetchone()
    return id


def add_enviroments(data, cursor):
    cursor.executemany("""INSERT INTO core_testenviroments (name, test_store_id_id)
                   VALUES (?, ?)""", [(name, data[1]) for name in data[0]])

    placeholders = ",".join("?" for _ in data[0])
    cursor.execute(f"""SELECT id FROM core_testenviroments 
                   WHERE name IN ({placeholders})""", data[0])
    temp = cursor.fetchall()
    id = [i[0] for i in temp]
    print(id)
    return id


def add_env_values(data, cursor):
    values = []
    keys = list(data[0].keys())
    for i in keys:
        value = data[0][i]
        values.append(value)
    print(values)

    cursor.execute("""INSERT INTO core_testvalues 
                   (eva_tp, suc_tp, env_tp, deg_tp, def_status, test_enviroments_id_id, date) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""", (*values, data[1], datetime.datetime.now()))
