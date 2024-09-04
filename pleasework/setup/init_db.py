import sqlite3;

conn = sqlite3.connect("assets/shop_data.db");

with open('setup/tihoi.sql') as f:
	conn.executescript(f.read());

cur = conn.cursor();

all_items = cur.execute("SELECT * FROM tbl_items").fetchall();

print(all_items);

conn.commit();

conn.close();