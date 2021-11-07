from os import name

from sqlalchemy.orm import backref
from voting import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length = 40), unique=True,nullable=False)
    department = db.Column(db.String(length = 40),nullable=False)
    email_address = db.Column(db.String(length = 40), unique=True, nullable=False)
    password_hash = db.Column(db.String(),nullable=False)
    hasVoted = db.Column(db.Boolean(),default = False)
    isAdmin = db.Column(db.Boolean, default =False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def vote_check(self):
        self.hasVoted = True
        db.session.commit()

    def has_user_voted(self):
        return self.hasVoted


    def is_user_admin(self):
        return self.isAdmin


class Candidate(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length = 40), unique=True,nullable=False)
    department = db.Column(db.String(length = 40),nullable=False)
    number_of_votes = db.Column(db.Integer(), default = 0)
    position = db.Column(db.String(), nullable = False)


    def __repr__(self):
        return f'{self.name}'

    def vote(self):
        self.number_of_votes += 1
        db.session.commit()

class Position(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    position = db.Column(db.String(), nullable = False, unique= True)
    def __repr__(self):
        return f'{self.position}'
    
    


    




