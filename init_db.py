from hello import app, db, User, Course
from werkzeug.security import generate_password_hash, check_password_hash
with app.app_context():
    db.drop_all()
    db.create_all()


    Max = User(username = "Max10", password_hash=generate_password_hash("Max123"), name="Max",role="student")
    db.session.add(Max)
    db.session.commit()

    DummyTeacher = User(username = "Adam2", password_hash=generate_password_hash("Adam123"), name="Adam",role="teacher")
    db.session.add(DummyTeacher)
    db.session.commit()

    Course1 = Course(name="Math101", professorID=DummyTeacher.id, time="MWF 10:00am-11:30am", capacity=10)
    db.session.add(Course1)
    db.session.commit()

    Course1.students.append(Max)

    db.session.commit()