from hello import app, db, User, Course
from werkzeug.security import generate_password_hash, check_password_hash
with app.app_context():
    db.drop_all()
    db.create_all()

    # Students
    Max = User(username = "Max10", password_hash=generate_password_hash("Max123"), name="Max",role="student")
    db.session.add(Max)

    Steven = User(username="Steven10", password_hash=generate_password_hash("Steven123"), name="Steven", role="student")
    db.session.add(Steven)
    
    # Teachers
    ProfessorAdam = User(username = "Adam2", password_hash=generate_password_hash("Adam123"), name="Adam",role="teacher")
    db.session.add(ProfessorAdam)

    ProfessorKyrilov = User(username = "Kyrilov22", password_hash=generate_password_hash("CSEKyrilov"), name="Angelo", role="teacher")
    db.session.add(ProfessorKyrilov)

    ProfessorKen = User(username = "Ken67", password_hash=generate_password_hash("WeLuvKen"), name="Ken", role="teacher")
    db.session.add(ProfessorKen)

    ProfessorWalker = User(username = "sWalker21", password_hash=generate_password_hash("luvWalkin"), name="Susan Walker", role="teacher")
    db.session.add(ProfessorWalker)

    ProfessorHepworth  = User(username = "Aworth76", password_hash=generate_password_hash("Walmart21"), name="Ammon Hepworth", role="teacher")
    db.session.add(ProfessorHepworth)
    
    AdminAccount = User(username = "Admin45", password_hash=generate_password_hash("Admin123"), name="Admin", role="admin")
    db.session.add(AdminAccount)

    db.session.commit()

    # Courses
    Course1 = Course(name="Math 101", professorID=ProfessorAdam.id, time="MWF 10:00am - 11:30am", capacity=100)
    db.session.add(Course1)

    Course1.students.append(Max)

    Course2 = Course(name="CSE 15", professorID=ProfessorKyrilov.id, time="TR 9:00am - 10:15am", capacity=105)
    db.session.add(Course2)

    Course2.students.append(Max)

    Course3 = Course(name="CSE 100", professorID=ProfessorKen.id, time="TR 1:00am - 2:15am", capacity=0)
    db.session.add(Course3)

    Course4 = Course(name="Physics 121", professorID=ProfessorWalker.id, time="TR 11:00am - 11:50am", capacity=10)
    db.session.add(Course4)

    Course5 = Course(name="CSE 108", professorID=ProfessorHepworth.id, time="MWF 2:00pm - 2:50pm", capacity=1)
    db.session.add(Course5)

    Course6 = Course(name="CSE 162", professorID=ProfessorHepworth.id, time="TR 3:00pm - 3:50pm", capacity=4)
    db.session.add(Course6)

    db.session.commit()