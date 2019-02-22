from flask import app, Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'myDB.sqlite3'
db = SQLAlchemy(app)


class User(db.Model):


    __tablename__ = 'users'
    #id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    #name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.String(20) , nullable=False)

    def __init__(self ,email, password):
        #self.name = name
        self.email = email
        self.password = password


    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password , password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)


    def __repr__(self):
        return '<User %r>' % self.email