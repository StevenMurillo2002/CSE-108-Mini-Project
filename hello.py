from flask_sqlalchemy import SQLAlchemy 
from flask import Flask, render_template, jsonify, request
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)


    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify(self, password):
        return check_password_hash(self.password_hash, password)
        



class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursenumber = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    professor = db.Column(db.String, unique=False, nullable=True)




from flask_admin.contrib.sqla import ModelView
app.secret_key = 'super secret key'

admin = Admin(app, name='Admin View')
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Classes, db.session))

@app.route('/')
def index():
    return render_template('index.html')




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)