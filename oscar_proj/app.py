from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error;

def get_db_connection():
    # Creating connection to database
    conn = None; 

    try:
        # Attempt to connect to the database
        conn = sqlite3.connect("assets/shop_data.db"); 
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

def cat_description_get():
    # Establish connection to the database and grab the cursor
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetching all content from tbl_items, filters, and filters_names
    all_items = cur.execute('SELECT * FROM tbl_items').fetchall()
    all_categories = cur.execute('SELECT * FROM tbl_filters').fetchall()
    all_filters = cur.execute('SELECT * FROM tbl_filters_names').fetchall()
    print("[LOG] - All items, filters, and filter names have been selected")
    print("---------------------------------------------------------------")
    cur.close()
    
    return all_items, all_categories, all_filters

# Function to update an item
def update_item(i_name):
    # Establishing a connection to the database
	conn = get_db_connection()
    # Code to execute in SQL
	sql = """
            UPDATE tbl_items SET
            name = ?,
            cost = ?,
            image = ?,
            stock = ?
            WHERE id = ?
            """
    # Execute the SQL code using the values in i_name
	conn.execute(sql, i_name).rowcount
	print(f"[LOG] - Updated item with name and values: {i_name}")
    # Committing the current action
	conn.commit()
    # Closing connection to database
	conn.close()

def update_name(n_name):
	conn = get_db_connection()
	sql = """
            UPDATE tbl_filters_names SET
            name = ?
            WHERE id = ?
            """
	conn.execute(sql, n_name)
	print(f"[LOG] - Updated filter name with title and ID: {n_name}")
	conn.commit()
	conn.close()

# Function to add an item
def add_item(i_data):
    conn = get_db_connection()
    # The sql execute code is change from update fields to adding fields
    sql = """
    INSERT INTO tbl_items 
    (name, cost, image, stock) 
    VALUES(?,?,?,?)"""
    # Execute the sql code with i_data while also using the lastrowid in order to make the new primary key ID
    conn.execute(sql, i_data).lastrowid    
    print(f"[LOG] - Added new item with name and values: {i_data}")
    conn.commit()
    conn.close()

def add_filter(f_data):
    conn = get_db_connection()
    sql = """
    INSERT INTO tbl_filters 
    (id, name_id) 
    VALUES(?,?)"""
    conn.execute(sql, f_data)
    print(f"[LOG] - Added new filter with values: {f_data}")
    conn.commit()
    conn.close()

def add_name(n_data):
    conn = get_db_connection()
    sql = """
    INSERT INTO tbl_filters_names (name) VALUES(?)
    """
    conn.execute(sql, (n_data,)).lastrowid
    print(f"[LOG] - Added new filter name with title and ID: {n_data}")
    conn.commit()
    conn.close()

def remove_name(n_item):
    conn = get_db_connection()
    sql = """
    DELETE FROM tbl_filters_names WHERE id = ? AND name = ?;
    """
    conn.execute(sql, n_item)
    print(f"[LOG] - Removed filter name with ID and name: {n_item}")
    conn.commit()
    conn.close()

def remove_filter(f_item):
    sql = """
    DELETE FROM tbl_filters WHERE id = ? and name_id = ?;
    """
    conn = get_db_connection()
    cur = conn.cursor();
    remove_filter_id = cur.execute(sql, f_item)
    print(f"[LOG] - Removed filter named: {remove_filter_id}")
    conn.commit()
    conn.close()

# Function to delete an item
def remove_item(i_item):
    # Deleting from the database using the DELETE function now
    sql = """
    DELETE FROM tbl_items WHERE id = ?;
    """
    conn = get_db_connection()
    cur = conn.cursor();
    remove_name_id = cur.execute(sql, i_item)
    print(f"[LOG] - Removed item with id: {remove_name_id}")
    conn.commit()
    conn.close()


app = Flask(__name__, static_url_path='/assets', static_folder='assets');

# Allows for a GET request if needed - but not used
@app.route("/", methods=['GET','POST'])
def index():

    # Setting data to cat_description_get so that I can specify which table to reference in the base.html
    data = cat_description_get()

    # This looks out for POST requests from modals
    if request.method == 'POST':
        # Find what action the modal was looking for, and execute the function for the action the modal stated below
        action = request.form.get("action")

        # If the modal was to edit an item
        if action == 'saveItemBtn':
            print("[LOG] - Processing POST request for editing an item")
            # Receiving the ID from the HTML form
            id = request.form.get('editID')
            # Specifying function i_name with values for each instance of ? in update_item(i_name)
            i_name = (
                request.form.get(f"editName{id}"),
                request.form.get(f"editCost{id}"),
	            request.form.get(f"editImage{id}"),
                request.form.get(f"editStock{id}"),
	            id
            )
            # Execute update_item(i_name)
            update_item(i_name)
            return redirect('/')
        
        if action == 'saveNameBtn':
            print("[LOG] - Processing POST request for editing a filter name")
            id = request.form.get('nameID')
            name = request.form.get(f'editName{id}')
            n_name = (name,id)
            update_name(n_name)
            return redirect('/')
        

      
        # If the modal was to add an item
        if action == 'add_item_form':
            print("[LOG] - Processing POST request to add an item")
            # Finding all values from the addItem___ inputs from the modals
            name = request.form.get("addItemName")
            cost = request.form.get("addItemCost")
            image = request.form.get("addItemImage")
            stock = request.form.get("addItemStock")
            # Specifying i_data with values for each instance of ? in add_item(i_data)
            i_data = (name,cost,image,stock)
            # Execute adding an item
            add_item(i_data)
            return redirect('/')
        
        if action == 'add_filter_form':
            print("[LOG] - Processing POST request to add a filter")
            id = request.form.get("addFilterID")
            name_id = request.form.get("addFilterNameID")
            f_data = (id, name_id)
            add_filter(f_data)
            return redirect('/')

        if action == 'add_filter_name_form':
            print("[LOG] - Processing POST request to add a filter name")
            n_data = request.form.get("addNameFilter")
            add_name(n_data)
            return redirect('/')

        if action == 'deleteFilterBtn':
            print("[LOG] - Processing POST request to delete a filter item")
            id = request.form.get("filterRemoveID")
            name_id = request.form.get("filterRemoveNameID")
            f_item = (id, name_id)
            remove_filter(f_item)
            return redirect('/')
        
        if action == 'deleteNameBtn':
            print("[LOG] - Processing POST request to delete a filter name")
            id = request.form.get("filterNameRemoveID")
            name_id = request.form.get("filterNameRemoveNameID")
            n_item = (id, name_id)
            remove_name(n_item)
            return redirect('/')

        # If the modal was to delete an item        
        if action == 'deleteItemBtn':
            print("[LOG] - Processing POST request to delete an item")
            # Find the id of the item to be deleted
            id = request.form.get("itemRemoveID")
            # ? = id
            i_item = (id)
            # Execute function to delete item
            remove_item(i_item)
            return redirect('/')

    # Processes base.html file using Jinja, and tables can be accessed using 'items', 'filters', and 'names'.
    return render_template("base.html", items=data[0], filters=data[1], names=data[2]);


if __name__ == "__main__":
	print("[LOG] - Single Page Application - Initialising")
    # Initialise Debugger
	app.run(debug=True);