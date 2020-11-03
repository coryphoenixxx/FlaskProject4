import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = os.urandom(1961)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)