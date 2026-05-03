from flask import Flask, render_template, request 
import sqlite3

app = Flask(__name__)


def get_db():
    return sqlite3.connect("users.db")


def create_table():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
         CREATE TABLE IF NOT EXISTS Users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   NAME TEXT,
                   Password TEXT
                   );
""")
    
    db.commit()
    db.close()

create_table()

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    msg =""
    if request.method == "post":
        username = request.form["username"]
        password =request.form["password"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM Users WHERE Name=?", (username,))
        account = cursor.fetchone()
        if account:
            msg = "Account already exists"
        else:
            cursor.execute("INSERT INTO Users (NAME, Password) VALUES (?, ?)" ,(username, password) )
            db.commit()
            msg = "You have successfully registered"
        db.close()
    return render_template("register.html", msg=msg)

@app.route("/Welcome")
def welcome():
    return render_template("welcome.html")



app.run(debug=True)