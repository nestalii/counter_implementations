from db import get_connection

conn = get_connection()
cursor = conn.cursor()

def reset_row():
    cursor.execute("UPDATE user_counter SET counter = 0, version = 0 WHERE user_id = 1")
    conn.commit()


def print_counter(name):
    cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1")
    print(f"Counter for {name} is {cursor.fetchone()[0]}\n")


def close_connection():
    cursor.close()
    conn.close()


def lost_update(conn):
    cursor = conn.cursor()

    for i in range(0, 10000):
        cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1")
        counter = cursor.fetchone()[0] + 1
        cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = %s", (counter, 1))
        conn.commit()

    cursor.close()
    conn.close()


def in_place_update(conn):
    cursor = conn.cursor()

    for i in range (0, 10000):
        cursor.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = %s", (1,))
        conn.commit()

    cursor.close()
    conn.close()


def row_level_locking(conn):
    cursor = conn.cursor()

    for i in range (0, 10000):
        cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE")
        counter = cursor.fetchone()[0] + 1
        cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = %s", (counter, 1))
        conn.commit()

    cursor.close()
    conn.close()


def optimistic_concurrency_control(conn):
    cursor = conn.cursor()

    for i in range (0, 10000):
        while True:
            cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1")
            (counter, version) = cursor.fetchone()
            counter += 1
            cursor.execute("UPDATE user_counter SET counter = %s, version = %s WHERE user_id = %s AND version = %s", (counter, version + 1, 1, version))
            conn.commit()
            count = cursor.rowcount
            if count > 0:
                break

    cursor.close()
    conn.close()