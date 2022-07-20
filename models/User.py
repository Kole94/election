class Users(db.Model):
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