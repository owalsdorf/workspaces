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

def base_table():
    conn = get_db_connection()
    cur = conn.cursor()
    sql = f"""
    SELECT * FROM tbl_items
    """
    all_items = cur.execute(sql).fetchall()

    conn.close

    return all_items

def get_items(searchinput, sortvar, sortcolumn):
    # Establish connection to the database and grab the cursor
    conn = get_db_connection()
    cur = conn.cursor()
    if searchinput == None:
        searchinput = ""
    if sortvar == None:
        sortvar = "DESC"
    if sortcolumn == None:
        sortcolumn = "sku"
    print("[LOG] - Attempting to execute SQL code")
    sql = f"""
    SELECT * FROM tbl_items 
    WHERE (id LIKE '%{searchinput}%'
    OR sku LIKE '%{searchinput}%'
    OR name LIKE '%{searchinput}%'
    OR cat LIKE '%{searchinput}%'
    OR size LIKE '%{searchinput}%'
    OR price LIKE '%{searchinput}%')
    ORDER BY {sortcolumn} {sortvar}
    """
    # Fetching all content from tbl_items, filters, and filters_names
    changed_items = cur.execute(sql).fetchall()
    print(f"[LOG] - Table has been updated. Sort type: {sortvar}, column sorted: {sortcolumn}, search input: {searchinput}.")
    print("---------------------------------------------------------------")
    conn.close()

    return changed_items;

app = Flask(__name__, static_url_path='/assets', static_folder='assets');

# Allows for a GET request if needed - but not used
@app.route("/", methods=['GET','POST'])
def index():

    # Setting data to get_items() so that I can specify which table to reference in the base.html
    sortcolumn = 'sku'
    sortvar = 'DESC'
    searchinput = '1'
    data = base_table()

    if request.method == 'POST':
        print("[LOG] - POST request detected")
        action = request.form.get("action")
       
        if action == 'sorting':
            print("[LOG] - Receiving post request to sort table")
            searchinput = request.form.get("search")
            sortvar = request.form.get("sortMethod")
            sortcolumn = request.form.get("sortColumn")
            data = get_items(searchinput, sortvar, sortcolumn)

        if action == 'searching':
            print("[LOG] - Receiving post request to search table")
            searchinput = request.form.get("search")
            print(f"[LOG] - Search input: {searchinput}")
            sortvar = request.form.get("sortMethod")
            sortcolumn = request.form.get("sortColumn")
            data = get_items(searchinput, sortvar, sortcolumn)

    # Processes base.html file using Jinja, and tables can be accessed using 'items', 'filters', and 'names'.
    return render_template("website.html", items=data, sortvar=sortvar, sortcolumn=sortcolumn, searchinput=searchinput);


if __name__ == "__main__":
	print("[LOG] - Search engine - Initialising")
    # Initialise Debugger
	app.run(debug=True, port=5050);