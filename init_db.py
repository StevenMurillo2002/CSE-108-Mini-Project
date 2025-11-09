from hello import app, db, User, Course
from werkzeug.security import generate_password_hash, check_password_hash
with app.app_context():
    db.drop_all()
    db.create_all()


    Max = User(username = "Max10", password_hash=generate_password_hash("Max123"), name="Max",role="student")
    db.session.add(Max)
    db.session.commit()

    ProfessorAdam = User(username = "Adam2", password_hash=generate_password_hash("Adam123"), name="Adam",role="teacher")
    db.session.add(ProfessorAdam)
    db.session.commit()

    ProfessorKyrilov = User(username = "Kyrilov22", password_hash=generate_password_hash("CSEKyrilov"), name="Angelo", role="teacher")
    db.session.add(ProfessorKyrilov)
    db.session.commit()

    AdminAccount = User(username = "Admin45", password_hash=generate_password_hash("Admin123"), name="Admin", role="admin")
    db.session.add(AdminAccount)
    db.session.commit()


    Course1 = Course(name="Math101", professorID=ProfessorAdam.id, time="MWF 10:00am-11:30am", capacity=100)
    db.session.add(Course1)
    db.session.commit()

    Course1.students.append(Max)

    Course2 = Course(name="CSE15", professorID=ProfessorKyrilov.id, time="TR 9:00am - 10:15am", capacity=105)
    db.session.add(Course2)
    db.session.commit()

    Course2.students.append(Max)


    db.session.commit()