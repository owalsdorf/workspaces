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

def get_items(columns, searchinput, sortvar, sortcolumn):
  # Establish connection to the database and grab the cursor
  conn = get_db_connection()
  cur = conn.cursor()
  sqlcolumns = ", ".join(columns)
  print("[LOG] - Attempting to execute SQL function")

  sql = f"""
  SELECT {sqlcolumns} FROM tbl_items
  WHERE (id LIKE '%{searchinput}%'
  OR sku LIKE '%{searchinput}%'
  OR name LIKE '%{searchinput}%'
  OR cat LIKE '%{searchinput}%'
  OR size LIKE '%{searchinput}%'
  OR price LIKE '%{searchinput}%')
  ORDER BY {sortcolumn} {sortvar}
  """
  # Fetching all content from tbl_items, filters, and filters_names
  changed_table = cur.execute(sql).fetchall()
  print(f"[LOG] - Table has been updated. Sort type: {sortvar}, column sorted: {sortcolumn}, search input: {searchinput}.")
  print(f"[LOG] - Columns selected: {sqlcolumns}.")
  print("---------------------------------------------------------------")
  conn.close()

  return changed_table;

app = Flask(__name__, static_url_path='/assets', static_folder='assets');

# Allows for a GET request if needed - but not used
@app.route("/", methods=['GET', 'POST'])
def index():
    # Default values
    sortcolumn = 'id'
    sortvar = 'ASC'
    searchinput = ''
    columns = ['id', 'sku', 'name', 'cat', 'size', 'price']
    data = get_items(columns, searchinput, sortvar, sortcolumn)

    if request.method == 'POST':
        print("[LOG] - POST request detected")
        action = request.form.get("action")
        print(f"[LOG] - Action type received: {action}")
        searchinput = request.form.get("search", "")
        sortvar = request.form.get("sortMethod", "ASC")
        sortcolumn = request.form.get("sortColumn", "id")
        columns = request.form.getlist("columns")

        # Ensure columns aren't empty
        if not columns:
            print(f"[LOG] - Columns are set to all off; preventing blank table")
            columns = ['id', 'sku', 'name', 'cat', 'size', 'price']

        if action == 'reset':
            print("[LOG] - Restoring to default settings.")
            sortcolumn = 'id'
            sortvar = 'ASC'
            searchinput = ''
            columns = ['id', 'sku', 'name', 'cat', 'size', 'price']
            data = get_items(columns, searchinput, sortvar, sortcolumn)

        elif action in ['filtering', 'sorting', 'searching']:
            data = get_items(columns, searchinput, sortvar, sortcolumn)

        print(f"[LOG] - Action: {action}, Search: {searchinput}, Sort: {sortvar}, Sort Column: {sortcolumn}, Columns: {columns}")

    return render_template("website.html", items=data, columns=columns)


if __name__ == "__main__":
  print("[LOG] - Search engine - Initialising")
  # Initialise Debugger
  app.run(debug=True, port=5050);