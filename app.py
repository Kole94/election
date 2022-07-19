import time
import os
# import redis
from flask import Flask, render_template, request,redirect, url_for,session
from sqlalchemy import  create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

app = Flask(__name__)
app.secret_key = "hello"

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string="sqlite:///"+os.path.join(BASE_DIR, 'site.db')
db = declarative_base()
engine = create_engine(connection_string, echo=True)

# cache = redis.Redis(host='redis', port=6379)

# def get_hit_count():
#     retries = 5
#     while True:
#         try:
#             return cache.incr('hits')
#         except redis.exceptions.ConnectionError as exc:
#             if retries == 0:
#                 raise exc
#             retries -= 1
#             time.sleep(0.5)

# @app.route('/')
# def hello():
#     count = get_hit_count()
#     return 'Hello World! I have been seen {} times.\n'.format(count)

class users(db):
    __tablename__="users"
    _id = Column("id", Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return "<h1>asdasd</h1>"

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        user = request.form["name"]
        session.permanet = True
        session["user"]= user
        # name = request.form["name"]
        # email = request.form["email"]
        # if:
        # else:
        abc = users(name="user",email="emial")
        db.session.add(abc)
        db.commit()
        # return redirect(url_for("user", user=user))
        return redirect(url_for("user"))


    if request.method == "GET":
        return render_template("register.html",abc="abc")

@app.route("/login",methods=["POST", "GET"])
def login(user):
    if request.method == "GET":
        user = users.query.filter_by(name=user)
        return render_template("login.html")
    # else:
        # name = request.form["name"]
        # email = request.form["email"]
        # # if:
        # # else:
        # user = users(name,"emial")
        # db.session.add(user)
        # db.commit()


@app.route("/user")
# def user(user):
# return f"<h1>{user}</h1>"
def user():
    if "user" in session:
        # user = session['user']
        user = users.query.filter_by(name=user).first()
        return f"<h1>{user}</h1>"


@app.route("/refresh",methods=["POST"])
def refresh():
    return "<h1>asdasd</h1>"

@app.route("/delete",methods=["POST"])
def delete():
    return "<h1>asdasd</h1>"

db.metadata.create_all(engine)
# app.run()
