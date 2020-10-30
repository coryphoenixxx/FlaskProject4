from datetime import datetime

from init import db


teachers_goals_association = db.Table('teachers_goals',
                                      db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
                                      db.Column('goal_id', db.Integer, db.ForeignKey('goals.id'))
                                      )


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.relationship("Goal", secondary=teachers_goals_association, back_populates="teachers")
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.REAL, nullable=False)
    timerecords = db.relationship("TimeRecord", back_populates="teacher")


class TimeRecord(db.Model):
    __tablename__ = 'timerecords'
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.relationship("Teacher", back_populates="timerecords")
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    dow = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    value = db.Column(db.Boolean, nullable=False)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    dow = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    teacher = db.relationship("Teacher")
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    goal = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)


class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    trans_title = db.Column(db.String, nullable=False, unique=True)
    image = db.Column(db.String, nullable=False, unique=True)
    teachers = db.relationship("Teacher", secondary=teachers_goals_association, back_populates='goals')
