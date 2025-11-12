from flask_sqlalchemy import SQLAlchemy 
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user, logout_user
from sqlalchemy import select, and_


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep it secret, keep it safe'


enrollment_table = db.Table('enrollment',
db.Column('student_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
db.Column('grade', db.String(8))
)

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
            if user.role == 'teacher':
                return redirect(url_for('teacher_courses'))
            else:
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

@app.route("/classes")
def view_all_classes():
    courses = Course.query.all()
    return render_template("classes.html", courses=courses)
    
@app.route('/student/add/<int:course_id>', methods=['POST'])
@login_required
def add_course(course_id):
    course = Course.query.get_or_404(course_id)

    # Check if enrolled already
    if current_user in course.students:
        flash('You are already enrolled in this course.', 'warning')
        return redirect(url_for('view_all_classes'))
    
    # Check if full
    if course.students.count() >= course.capacity:
        flash('Course Full.', 'alert')
        return redirect(url_for('view_all_classes'))
    
    # Enroll student
    course.students.append(current_user)
    flash('Enrolled Successfully!', 'success')
    db.session.commit()
    
    return redirect(url_for('view_all_classes'))

@app.route('/student/drop/<int:course_id>', methods=['POST'])
@login_required
def drop_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Check if enrolled already
    if current_user in course.students:
        course.students.remove(current_user)
        flash('Dropped Successfully!', 'success')
        db.session.commit()
    else:
        flash('Course not Dropped', 'alert')
        
    return redirect(url_for('view_all_classes'))


# @app.route('/teacher/dashboard')
# @login_required
# def teach_dash():

@app.route('/teacher/courses')
@login_required
def teacher_courses():
    if current_user.role != 'teacher':
        flash('Unauthorized: teachers only.', 'alert')
        return redirect(url_for('student_courses'))
    courses = Course.query.filter_by(professorID=current_user.id).all()
    return render_template('teacher_courses.html', courses=courses)


@app.route('/teacher/course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def teacher_course(course_id):
    # must be a teacher and must own this course
    if current_user.role != 'teacher':
        flash('Unauthorized: teachers only.', 'alert')
        return redirect(url_for('student_courses'))

    course = Course.query.get_or_404(course_id)
    if course.professorID != current_user.id:
        flash('You do not teach this course.', 'alert')
        return redirect(url_for('teacher_courses'))

    if request.method == 'POST':
        student_id = int(request.form['student_id'])
        grade = (request.form.get('grade') or '').strip()

        # ensure the student is actually enrolled
        exists = db.session.execute(
            select(enrollment_table.c.student_id)
            .where(and_(enrollment_table.c.student_id == student_id,
                        enrollment_table.c.course_id  == course_id))
        ).first()
        if not exists:
            flash('Student is not enrolled in this course.', 'alert')
            return redirect(url_for('teacher_course', course_id=course_id))

        # update the grade in the enrollment row
        db.session.execute(
            enrollment_table.update()
            .where(and_(enrollment_table.c.student_id == student_id,
                        enrollment_table.c.course_id  == course_id))
            .values(grade=grade if grade else None)
        )
        db.session.commit()
        flash('Grade saved!')
        return redirect(url_for('teacher_course', course_id=course_id))

    # build grades_map from the enrollment table for this course
    rows = db.session.execute(
        select(enrollment_table.c.student_id, enrollment_table.c.grade)
        .where(enrollment_table.c.course_id == course_id)
    ).fetchall()
    grades_map = {(sid, course_id): g for (sid, g) in rows}

    return render_template('teacher_course.html', course=course, grades_map=grades_map)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)