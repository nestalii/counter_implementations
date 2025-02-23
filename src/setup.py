from db import get_connection

conn = get_connection()

cur = conn.cursor()

cur.execute("CREATE TABLE user_counter (user_id SERIAL PRIMARY KEY, counter INTEGER, version INTEGER);")

cur.execute("INSERT INTO user_counter (counter, version) VALUES (%s, %s)", (0, 0))

conn.commit()

cur.close()
conn.close()