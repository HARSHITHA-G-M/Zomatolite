from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="rootpassword",
        database="zomatolite"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        db.commit()
        return redirect("/login")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            return redirect("/restaurants")
        else:
            return "Invalid credentials"
    return render_template("login.html")

@app.route("/restaurants")
def restaurants():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM restaurants")
    data = cursor.fetchall()
    return render_template("restaurants.html", restaurants=data)

@app.route("/menu/<int:restaurant_id>")
def menu(restaurant_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu WHERE restaurant_id = %s", (restaurant_id,))
    items = cursor.fetchall()
    return render_template("menu.html", items=items)

@app.route("/order/<int:menu_id>")
def order(menu_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO orders (menu_id) VALUES (%s)", (menu_id,))
    db.commit()
    return redirect("/orders")

@app.route("/orders")
def orders():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.id, m.item_name, r.name as restaurant 
        FROM orders o 
        JOIN menu m ON o.menu_id = m.id 
        JOIN restaurants r ON m.restaurant_id = r.id
    """)
    all_orders = cursor.fetchall()
    return render_template("orders.html", orders=all_orders)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

