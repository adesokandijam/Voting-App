from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Voting.db'
app.config['SECRET_KEY'] = 'HARD TO GUESS STRING'
db = SQLAlchemy(app)
db.create_all()
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = "info"
from voting import routes
