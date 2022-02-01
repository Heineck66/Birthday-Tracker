import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from sqlalchemy.sql.expression import null

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        post = request.form.getlist('birth')
        newbd = {'name': post[0], 'month': post[1], 'day': post[2]}

        if newbd != null:
            for k in newbd:
                if newbd[k] == '':
                    print('\nnewbd is invalid!\n')
                    return render_template('fail.html')
        else:
            print('Request was NULL')
            return render_template('fail.html')

        db.execute('INSERT INTO birthdays (name,month,day) VALUES (?,?,?)',
                   newbd['name'], newbd['month'], newbd['day'])

        return redirect("/")

    else:
        births = db.execute('SELECT * FROM birthdays;')

        return render_template("index.html", births=births)


@app.route("/delete", methods=['POST'])
def remove():
    id = request.form.get('id')
    db.execute('DELETE FROM birthdays WHERE id = ?', id)

    return redirect('/')


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':

        post = request.form.getlist('birth')
        id = request.form.get('id')

        newbd = {'name': post[0], 'month': post[1], 'day': post[2]}

        if newbd != null:
            for k in newbd:
                if newbd[k] == '':
                    print('\nnewbd is invalid!\n')
                    return render_template('fail.html')
        else:
            print('Request was NULL')
            return render_template('fail.html')

        db.execute('UPDATE birthdays SET name=?, month=?,day=? WHERE id=?',
                   newbd['name'], newbd['month'], newbd['day'], id)

        return redirect('/')
    else:
        id = request.args.get('id')
        name = request.args.get('name')

        births = db.execute('SELECT * FROM birthdays;')

        return render_template('edit.html', births=births, name=name, id=id)
