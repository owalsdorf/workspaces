from Flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error;

def get_db_connection():
	""" create connection to database """
	conn = None

	try:
		conn = sqlite3.connect("assets/shop_data.db")
		print("[LOG] connected")
		print("[LOG]",sqlite3.version)
	except Error as er:
		print(er)

	conn.row_factory = sqlite3.Row
	return conn


def cat_description_get():
    conn = get_db_connection()
    cur = conn.cursor()

    print("[LOG] - getting all items")
    all_items = cur.execute('SELECT * FROM tbl_items').fetchall()
    print("[LOG] - receiving all filters")
    all_categories = cur.execute('SELECT * FROM tbl_filters').fetchall()
    print("[LOG] - getting all filter names")
    all_filters = cur.execute('SELECT * FROM tbl_filters_names').fetchall()
    cur.close()
    return all_items, all_categories, all_filters

app = Flask(__name__, static_url_path='/assets', static_folder='assets');

@app.route("/", methods=['GET','POST'])
def index():

    data = {};

    if request.method == 'POST':
        print("[LOG] - processing POST request")
        if request.form.get('saveItemBtn') == request.form.get('editItemID'):
                id = request.form.get('editItemID')
                print(request.form.get(f"editItemDescription{id}"))

    if request.method == 'GET':
        print("[LOG] - processing get message")
        # conn = get_db_connection();
        # cur = conn.cursor();
        # print("[LOG] - getting all items")
        # all_items = cur.execute('SELECT * FROM tbl_items').fetchall();
        # data = all_items
        data = cat_description_get()

        # message = "Welcome to the Tihoi Shop";
    return render_template("base.html", items=data[0], filters=data[1], names=data[2]);
    #return render_template("base.html", data=data)
        # return render_template("base.html")

# running
if __name__ == "__main__":
	print("[LOG] its happening")
	app.run(debug=True);