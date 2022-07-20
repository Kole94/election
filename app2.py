# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

# db.create_all()
# admin = User(username='admin', email='admin@example.com')
# db.session.add(admin)
# db.session.commit()
# User.query.all()
# print("dasdasdasdasdsadsa")
# User.query.all()
print('dsadasds')

def split(word):
        return [char for char in word]

def validate_jmbg(jmbg):
       
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

