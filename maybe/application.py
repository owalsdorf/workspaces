from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error;

def get_db_connection():
    # Creating connection to database
    conn = None; 

    try:
        # Attempt to connect to the database
        conn = sqlite3.connect("maybe/assets/shopped_data.db"); 
        print("---------------------------------------------------------------")
        print("[LOG] - Connected to database. Version", sqlite3.version); 
    # If there is no connection, print an error
    except Error as er:
        print(er);

    # Enable row factory
    conn.row_factory = sqlite3.Row; 
    
    # Enforce referential Integrity
    sql = """
            PRAGMA foreign_keys = ON
            """
    conn.execute(sql);
    return conn

def get_items():
    # Establish connection to the database and grab the cursor
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetching all content from tbl_items, filters, and filters_names
    all_items = cur.execute('SELECT * FROM tbl_items').fetchall()
    print("[LOG] - All items have been selected")
    print("---------------------------------------------------------------")
    cur.close()
    
    return all_items
    


app = Flask(__name__, static_url_path='/assets', static_folder='assets');

# Allows for a GET request if needed - but not used
@app.route("/", methods=['GET','POST'])
def index():

    # Setting data to cat_description_get so that I can specify which table to reference in the base.html
    data = get_items()

    # Processes base.html file using Jinja, and tables can be accessed using 'items', 'filters', and 'names'.
    return render_template("website.html", items=data);


if __name__ == "__main__":
	print("[LOG] - Single Page Application - Initialising")
    # Initialise Debugger
	app.run(debug=True);