from contextlib import nullcontext
from functools import wraps
import json
from multiprocessing import connection
import os
from werkzeug.utils import secure_filename
from xml.dom.minidom import Identified
from flask import Flask, render_template, request,redirect, url_for,session, make_response,jsonify,Response
from sqlalchemy import  Column, Integer, String, Boolean, ARRAY
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
# import jwt
from datetime import timedelta;
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token,get_jwt_identity,get_jwt;
import redis
from rq import Worker, Queue, Connection
import csv
import codecs

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY##@sdfd"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'transactions.db' 
db = SQLAlchemy(app)

jwtM = JWTManager(app)
r = redis.Redis(host='redis',port=6379)
q = Queue(connection=r)

def split(word):
        return [char for char in word]
 
class User(db.Model):
    __tablename__="users"
    _id = Column("id", Integer, primary_key=True)
    jmbg = Column(String(256))
    forename = Column(String(256))
    surname = Column(String(256))
    email = Column(String(256))
    password = Column(String(256))

    

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            return render_template('error.html',statusCode=400, message=email)

            # raise ValueError("failed simple email validation")
        return email

    @validates('forename')
    def validate_forename(self, key, forename):
        if forename == None:
            raise ValueError("you mast provide forename")
        return forename

    @validates('surename')
    def validate_surename(self, key, surename):
        if surename == None:
            raise ValueError("you mast provide surename")
        return surename

    @validates('jmbg')
    def validate_jmbg(self, key, jmbg):

        if jmbg == None:
            raise ValueError("you mast provide jmbg")

       
        jmbgList = split(jmbg)
        if (len(jmbgList) != 13):
                return render_template('error.html',statusCode=400, message=len(jmbgList))

            # raise ValueError("Jmbg ne sadrzi odgovarajuci broj karaktera")
        
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
            return render_template('error.html',statusCode=400, message=len(password))
        return password

    def getPassword(self):
        return self.password

    def __init__(self, email,jmbg,forename, surname, password):
        self.jmbg = jmbg
        self.forename = forename
        self.surname = surname
        self.email = email
        self.password = password


def deamon(election, party):
    return 


@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        try:
            request_data = request.get_json()

            forename = request_data["forename"]
            surename = request_data["surename"]
            jmbg = request_data["jmbg"]
            email = request_data["email"]
            password = request_data["password"]
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
            request_data = request.get_json()
            email = request_data["email"]
            password = request_data["password"]
            user = User.query.filter_by(email=email).first()
            if(user.getPassword() == password):
                accessToken = create_access_token(identity=email, additional_claims={"user":"abc"},expires_delta=timedelta(minutes=30)) 
                refreshToken = create_refresh_token(identity=email,  additional_claims={"user":"abc"})            
                return jsonify(token= accessToken, refresh=refreshToken)
        except ValueError as e:
            return render_template('error.html',statusCode=400, message=e)


@app.route("/user",methods=["GET"])
@jwt_required()
def user():
    try:
        return f"<div><h1>ok</h1></div>"
    except ValueError as e:
        return render_template('error.html',statusCode=400, message=e)


@app.route("/refresh",methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity=get_jwt_identity()
    refreshClaims=get_jwt()

    return Response (create_access_token(identity=identity,  additional_claims={"user":"abc"}), status=200)         


# @app.route("/delete",methods=["POST"])
# def delete():
#     return "<h1>asdasd</h1>"




class ElectionParticipant(db.Model):
    __tablename__="electionParticipant"
    _id = Column("id", Integer, primary_key=True)
    forename = Column(String(256))
    individual = Column(Boolean)
    # id = Column(Integer)



    def __init__(self, forename, individual):
        self.forename = forename
        self.individual = individual
        # self.id = id

class Election(db.Model):
    __tablename__="election"
    _id = Column("id", Integer, primary_key=True)
    start = Column(String(256))
    end = Column(String(256))
    individual = Column(Boolean)
    participants = ARRAY(Integer)

    def __init__(self, start, end, individual, participants):
        self.start = start
        self.end = end
        self.individual = individual
        self.participants = participants

@app.route("/createParticipan",methods=["POST"])
# @jwt_required()
def createParticipan():
    request_data = request.get_json()

    forename = request_data["forename"]
    individual = request_data["individual"]
    try:
        participant = ElectionParticipant(forename=forename, individual=individual)
        db.session.add(participant)
        db.session.commit()
        return jsonify(forename=forename)
    except ValueError as e:
            return e

def log(electionParticipant):
    return jsonify(id=electionParticipant._id, name=electionParticipant.forename)




@app.route("/getParticipants",methods=["GET"])
# @jwt_required()
def getParticipants():
    electionParticipants = ElectionParticipant.query.all()

    result = []

    for p in electionParticipants:
        participant = {
            "id": p._id,
            "name": p.forename,
            "individual": p.individual
        }
        result.append(participant)


    return jsonify(participants=result)      


@app.route("/createElection",methods=["POST"])
# @jwt_required()
def createElection():
    request_data = request.get_json()
    start = request_data["start"]
    end = request_data["end"]
    individual = request_data["individual"]
    participants = request_data["participants"]
    election = Election(start=start,end=end, individual=individual, participants=participants)
    db.session.add(election)
    db.session.commit()
    return render_template("login.html")

@app.route("/getElections",methods=["GET"])
# @jwt_required()
def getElections():
    electionParticipants = ElectionParticipant.query.all()
    election = Election.query.all()
    result = []

    for e in election:
        participantsList = []
        for p in electionParticipants:
            particiant = {"id": p._id, "name": p.forename}
            participantsList.append(particiant)

        election = {
            "start": e.start,
            "end": e.end,
            "individual": e.individual,
            "participants": participantsList
        }
        result.append(election)


    return jsonify(participants=result) 




@app.route("/vote",methods=["POST"])
# @jwt_required()
def vote():
    data = []
    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['file'] # This line uses the same variable and worked fine
            stre = uploaded_file.readlines()
            data = str(stre).replace("b","").replace("'","").replace("\\n","").replace(" ","").replace("[","").replace("]","").split(',')
            # r.rpush("election", data[0],data[2])
            job = q.enqueue(deamon, data[0],data[2])
            return job.id
    


            # filepath = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
            # uploaded_file.save(filepath)
            # with open(filepath) as file:
            #     csv_file = csv.reader(file)
            #     for row in csv_file:
            #         data.append(row)
            # return redirect(request.url)
            # return Response ("csv_file", status=200)         



@app.route("/getElectionResult/<id>",methods=["GET"])
# @token_required
def getElectionResult(id):
    list = r.lrange(id, 0, -1)

    return jsonify(str(list))

# @app.route("/getResult/<id>",methods=["GET"])
# @token_required
# def getResult(id):
#     elections = Election.query.filtery_by(id=id).firts()
#     return elections

# @app.route("/vote",methods=["POST"])
# @token_required
# def vote(id):
#     guid = request.form["guid"]
#     voteFor = request.form["voteFor"]
    # db.session.add()
    # Go to redis
    # elections = Election.query.filtery_by(id=id).firts()
    # return elections






SQLAlchemy.create_all(db)
app.run()
