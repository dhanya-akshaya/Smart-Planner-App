from flask import Flask,render_template,request,redirect
import sqlite3

app=Flask(__name__)

def connect():
    return sqlite3.connect("planner.db")

def create_table():

    con=connect()

    cur=con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    due TEXT,
    priority TEXT,
    status TEXT)
    """)

    con.commit()

    con.close()

create_table()

@app.route("/")
def index():

    con=connect()

    cur=con.cursor()

    cur.execute("SELECT * FROM tasks")

    tasks=cur.fetchall()

    con.close()

    return render_template("index.html",tasks=tasks)


@app.route("/add",methods=["POST"])
def add():

    task=request.form["task"]

    date=request.form["date"]

    time=request.form["time"]

    priority=request.form["priority"]

    due=date+" "+time

    con=connect()

    cur=con.cursor()

    cur.execute(
    "INSERT INTO tasks(task,due,priority,status) VALUES(?,?,?,?)",
    (task,due,priority,"Pending")
    )

    con.commit()

    con.close()

    return redirect("/")


@app.route("/complete/<int:id>")
def complete(id):

    con=connect()

    cur=con.cursor()

    cur.execute(
    "UPDATE tasks SET status=? WHERE id=?",
    ("Done",id)
    )

    con.commit()
    con.close()
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):

    con=connect()

    cur=con.cursor()

    cur.execute(
    "DELETE FROM tasks WHERE id=?",
    (id,)
    )

    con.commit()

    con.close()

    return redirect("/")


if __name__=="__main__":
    app.run()
