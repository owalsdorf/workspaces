import sqlite3;

# Creates connection to the database
with sqlite3.connect("maybe/assets/shopped_data.db") as conn:
	# Run our sql to initialise the database, using with_resources pattern
	with open('maybe/setup/coffee.sql') as f:
		conn.executescript(f.read());

	# Grab cursor
	cur = conn.cursor();

	# Run test SQL to make sure that everything is working properly
	all_items = cur.execute("SELECT * FROM tbl_items").fetchall();
	# Display the table
	print(all_items);

	# Save changes to database
	conn.commit();