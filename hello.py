from flask_sqlalchemy import SQLAlchemy 
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user, logout_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep it secret, keep it safe'


enrollment_table = db.Table('enrollment',
db.Column('student_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True))




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    classenrolled = db.relationship('Course', secondary=enrollment_table, backref=db.backref('students', lazy='dynamic'), lazy='dynamic')

    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify(self, password):
        return check_password_hash(self.password_hash, password)
        



class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    professorID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professor = db.relationship('User', foreign_keys=[professorID], backref='courses_taught') 
    time = db.Column(db.String(64),nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def get_student_count(self):
        return self.students.count()

    
    # def is_full(self):
    #     self.capacity = capacity
        


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



from flask_admin.contrib.sqla import ModelView
app.secret_key = 'super secret key'

admin = Admin(app, name='Admin View')
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Course, db.session))

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student_courses'))
    
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        user = User.query.filter_by(username=username).first()
        if user is None or not user.verify(password):
            return redirect(url_for('login'))
        if user and user.verify(password):
            login_user(user)
            return redirect(url_for('student_courses'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  
    return redirect(url_for('login'))

@app.route('/student/courses')
@login_required
def student_courses():
    allcourses = current_user.classenrolled.all()
    return render_template('student_courses.html', courses=allcourses)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)