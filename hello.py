from flask_sqlalchemy import SQLAlchemy 
from flask import Flask, render_template, jsonify, request
from flask_admin import Admin


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)

from flask_admin.contrib.sqla import ModelView
app.secret_key = 'super secret key'

admin = Admin(app, name='microblog')
admin.add_view(ModelView(User,db.session))

@app.route('/')
def index():
    return render_template('index.html')


app.run()