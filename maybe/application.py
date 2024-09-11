from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error;

def get_db_connection():
    # Creating connection to database
    conn = None; 

    try:
        # Attempt to connect to the database
        conn = sqlite3.connect("assets/shopped_data.db"); 
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

def get_items(sortvar, sortcolumn):
    # Establish connection to the database and grab the cursor
    conn = get_db_connection()
    sql = f"""
    SELECT * FROM tbl_items ORDER BY {sortcolumn} {sortvar}
    """
    # Fetching all content from tbl_items, filters, and filters_names
    all_items = conn.execute(sql).fetchall()
    print(f"[LOG] - Items have been sorted by {sortvar}")
    print("---------------------------------------------------------------")
    conn.close()

    return all_items
    

app = Flask(__name__, static_url_path='/assets', static_folder='assets');

# Allows for a GET request if needed - but not used
@app.route("/", methods=['GET','POST'])
def index():

    # Setting data to get_items() so that I can specify which table to reference in the base.html
    sortcolumn = "id"
    sortvar = "ASC"
    data = get_items(sortvar, sortcolumn)

    if request.method == 'POST':
        action = request.form.get("action")

        if action == 'getvariables':
            print("[LOG] - Receiving post request to determine variables")
            sortvar = request.form.get("sortMethod")
            sortcolumn = request.form.get("sortColumn")
            data = get_items(sortvar, sortcolumn)
    
    # Processes base.html file using Jinja, and tables can be accessed using 'items', 'filters', and 'names'.
    return render_template("website.html", items=data);


if __name__ == "__main__":
	print("[LOG] - Search engine - Initialising")
    # Initialise Debugger
	app.run(debug=True, port=5050);