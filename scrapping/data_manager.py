import sqlite3
import datetime


def data_manager(data):
    # Connection
    with sqlite3.connect("../monitor/db.sqlite3") as conn:
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
                    for env_name, env_data in data[store].items():
                        values = (
                            env_data,
                            res[env_name]
                        )
                        add_env_values(values, cursor)
                    conn.commit()
                    print(f"{store}: OK!")


def add_store(data, cursor):
        cursor.execute("""SELECT id FROM core_teststore
                   WHERE name = ?""", (data,))
        id = cursor.fetchone()

        if id:
            return id
        else:
            cursor.execute("""INSERT INTO core_teststore (name)
                        VALUES (?)""", (data,))
            
            cursor.execute("""SELECT id FROM core_teststore
                        WHERE name = ?""", (data,))
            id = cursor.fetchone()
            return id


def add_enviroments(data, cursor):
        placeholders = ",".join("?" for _ in data[0])
        cursor.execute(f"""SELECT id, name FROM core_testenviroments 
                    WHERE name IN ({placeholders})
                    AND test_store_id_id = ?""", (*data[0], data[1]))
        temp = cursor.fetchall()
        
        env_map = {
            name: id_
            for id_, name in temp
        }

        if len(env_map) == len(data[0]):
            return env_map
        else:
            missing = [
                 env
                 for env in data[0]
                 if env not in env_map
            ]

            cursor.executemany("""INSERT INTO core_testenviroments (name, test_store_id_id)
                        VALUES (?, ?)""", [(name, data[1]) for name in missing])

            placeholders = ",".join("?" for _ in data[0])
            cursor.execute(f"""SELECT id, name FROM core_testenviroments 
                        WHERE name IN ({placeholders})
                        AND test_store_id_id = ?""", (*data[0], data[1]))
            temp = cursor.fetchall()
            
            env_map = {
                name: id_
                for id_, name in temp
            }
            return env_map


def add_env_values(data, cursor):
    values = []
    keys = list(data[0].keys())
    for i in keys:
        value = data[0][i]
        values.append(value)

    cursor.execute("""INSERT INTO core_testvalues 
                   (eva_tp, suc_tp, env_tp, deg_tp, def_status, test_enviroments_id_id, date) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""", (*values, data[1], datetime.datetime.now()))
