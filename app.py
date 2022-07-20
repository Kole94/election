import time
import os
from flask import Flask, render_template, request,redirect, url_for,session
from sqlalchemy import  Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'transactions.db' 
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__="users"
    _id = Column("id", Integer, primary_key=True)
    jmbg = Column(String(100))
    forename = Column(String(256))
    surname = Column(String(256))
    email = Column(String(256))
    password = Column(String(256))

    def getName(self):
        return self.name

    def __init__(self, email,jmbg,forename, surname, password):
        self.email = email
        # 13 karaktera
        self.jmbg = jmbg
        self.forename = forename
        self.surname = surname
        self.email = email
        self.password = password

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        forename = request.form["forename"]
        surename = request.form["surename"]
        jmbg = request.form["jmbg"]
        email = request.form["email"]
        password = request.form["password"]
        user = User(forename=forename,email=email,
        jmbg=jmbg,password=password, surname=surename)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user"))

    if request.method == "GET":
        return render_template("register.html",abc="abc")

@app.route("/login",methods=["POST", "GET"])
def login(user):
    if request.method == "GET":
        user = User.query.filter_by(name=user)
        return render_template("login.html",
        forename = "forename",surename = "surename",
        jmbg = "jmbg",email = "email",password = "password")
    # else:
        # name = request.form["name"]
        # email = request.form["email"]
        # # if:
        # # else:
        # user = users(name,"emial")
        # db.session.add(user)
        # db.commit()


@app.route("/user")
def user():
    peter = User.query.filter_by(forename='peter').first()
    m = peter.email
    return f"<div><h1>{m}</h1></div>"


# @app.route("/refresh",methods=["POST","GET"])
# def refresh():
#     return "<h1>asdasd</h1>"

# @app.route("/delete",methods=["POST"])
# def delete():
#     return "<h1>asdasd</h1>"

SQLAlchemy.create_all(db) 
app.run()
