from flask import render_template
import random

from init import db, app
from models import Teacher, TimeRecord, Booking, Request, Goal
from forms import RequestForm, BookingForm
import data


@app.route('/')
def render_index():
    random_teachers = db.session.query(Teacher).all()
    goals = db.session.query(Goal).all()
    random.shuffle(random_teachers)
    return render_template('index.html', teachers=random_teachers[:6], goals=goals)


@app.route('/goals/<goal>/')
def render_goal(goal):
    local_goal = db.session.query(Goal).filter(Goal.title==goal).first_or_404()
    teachers = sorted(local_goal.teachers, key=lambda t: t.rating, reverse=True)
    goals = db.session.query(Goal).all()
    return render_template('goal.html', teachers=teachers, goals=goals, goal=local_goal)


@app.route('/profiles/<int:id>/')
def render_profile(id):
    teacher = db.session.query(Teacher).get_or_404(id)
    timetable = data.create_timetable(db.session.query(TimeRecord).
                                      filter((TimeRecord.teacher_id==id) & (TimeRecord.value)).all())
    return render_template('profile.html', teacher=teacher, tt=timetable, times=data.teacher_times, wd=data.week_days)


@app.route('/booking/<int:id>/<day_of_week>/<time>/', methods=['GET', 'POST'])
def render_booking(id, day_of_week, time):
    form = BookingForm()

    if form.validate_on_submit():
        id = form.teacher_id.data
        client = {
            'dow': form.dow.data,
            'time': form.time.data,
            'name': form.name.data,
            'phone': form.phone.data,
            'teacher_id': id
        }

        booking = Booking(
            dow=client['dow'],
            time=client['time'],
            name=client['name'],
            phone=client['phone'],
            teacher_id=client['teacher_id']
        )

        db.session.add(booking)
        teacher = db.session.query(Teacher).get_or_404(id)
        timerecord = db.session.query(TimeRecord).filter((TimeRecord.teacher_id == id) &
                                                         (TimeRecord.dow==client['dow']) &
                                                         (TimeRecord.time==client['time'])).first_or_404()
        timerecord.value = False
        db.session.commit()
        return render_template('booking_done.html', client=client, picture=teacher.picture, wd=data.week_days)

    teacher = db.session.query(Teacher).get_or_404(id)
    return render_template('booking.html', teacher=teacher, wd=data.week_days, dow=day_of_week, time=time,
                           form=form)


@app.route('/request/', methods=['GET', 'POST'])
def render_request():
    form = RequestForm()
    goals = db.session.query(Goal).all()
    form.goals.choices = [(g.title, g.image + g.trans_title) for g in goals]

    if form.validate_on_submit():
        client = {
            'name': form.name.data,
            'phone': form.phone.data,
            'goal': form.goals.data,
            'time': form.times.data
        }

        request_for_teacher = Request(
            name=client['name'],
            phone=client['phone'],
            goal=client['goal'],
            time=client['time']
        )

        db.session.add(request_for_teacher)
        db.session.commit()

        goal = db.session.query(Goal).filter(Goal.title==client['goal']).first_or_404()

        return render_template('request_done.html', client=client, goal=goal)
    return render_template('request.html', ctimes=data.client_times, form=form)


@app.errorhandler(404)
def page_404(e):
    return render_template('404.html', error=e), 404


if __name__ == '__main__':
    app.run()
