import time
import os
from flask import Flask, render_template, request,redirect, url_for,session
from sqlalchemy import  Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

app = Flask(__name__)
app.secret_key = "hello"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'transactions.db' 
db = SQLAlchemy(app)

def split(word):
        return [char for char in word]

class User(db.Model):
    __tablename__="users"
    _id = Column("id", Integer, primary_key=True)
    jmbg = Column(Integer())
    forename = Column(String(256))
    surname = Column(String(256))
    email = Column(String(256))
    password = Column(String(256))

    

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("failed simple email validation")
        return email
    @validates('forename')

    def validate_forename(self, key, forename):
        if len(forename) == 0:
            raise ValueError("you mast provide forename")
        return forename

    @validates('surename')
    def validate_surename(self, key, surename):
        if len(surename) == 0:
            raise ValueError("you mast provide surename")
        return surename

    @validates('jmbg')
    def validate_jmbg(self, key, jmbg):
       
        jmbgList = split(jmbg)
        if (not(len(jmbgList) == 13)):
            raise ValueError("Jmbg ne sadrzi odgovarajuci broj karaktera")
        
        dd= int(jmbgList[0] + jmbgList[1])
        mm= int(jmbgList[2] + jmbgList[3])
        yyy= int(jmbgList[4] + jmbgList[5] + jmbgList[6])
        rr= int(jmbgList[7] + jmbgList[8])
        bbb= int(jmbgList[9] + jmbgList[10] + jmbgList[11])

        m = 11 - (( 7*(int(jmbgList[0]) + int(jmbgList[6])) 
        + 6*(int(jmbgList[1]) + int(jmbgList[7])) 
        + 5*(int(jmbgList[2]) + int(jmbgList[8])) 
        + 4*(int(jmbgList[3]) + int(jmbgList[9])) 
        + 3*(int(jmbgList[4])+ int(jmbgList[10])) 
        + 2*(int(jmbgList[5]) + int(jmbgList[11]))) % 11)

        k = m if 1 <= m <= 9 else 0
        print(k, jmbgList[12] , dd , mm, yyy, rr, bbb)
        if (dd > 31 or mm > 12 or yyy > 999 or not(70 < rr < 90) 
        or not(0 <= bbb <= 500 or 500 <= bbb <= 999) or not(int(jmbgList[12]) == k )):
            raise ValueError("failed simple jmbg validation")
        return jmbg

    @validates('password')
    def validate_password(self, key, password):
        if (len(password) < 8):
            raise ValueError("failed simple password validation")
        return password

    def getPassword(self):
        return self.password

    def __init__(self, email,jmbg,forename, surname, password):
        self.jmbg = jmbg
        self.forename = forename
        self.surname = surname
        self.email = email
        self.password = password

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        try:

            forename = request.form["forename"]
            surename = request.form["surename"]
            jmbg = request.form["jmbg"]
            email = request.form["email"]
            password = request.form["password"]
            user = User(forename=forename,email=email,
            jmbg=jmbg,password=password, surname=surename)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        except ValueError as e:
            return render_template('error.html',statusCode=400, message=e)


    if request.method == "GET":
        return render_template("register.html")

@app.route("/login",methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    else:
        try:
            peter = User.query.filter_by(email=request.form["email"]).first()
            if(peter.getPassword() == request.form["password"]):
                return redirect(url_for("user"))
        except ValueError as e:
            return render_template('error.html',statusCode=400, message=e)


@app.route("/user")
def user():
    return f"<div><h1>ok</h1></div>"


# @app.route("/refresh",methods=["POST","GET"])
# def refresh():
#     return "<h1>asdasd</h1>"

# @app.route("/delete",methods=["POST"])
# def delete():
#     return "<h1>asdasd</h1>"

SQLAlchemy.create_all(db) 
app.run()
