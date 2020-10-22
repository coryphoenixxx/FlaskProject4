week_days = {'mon': 'Понедельник',
             'tue': 'Вторник',
             'wed': 'Среда',
             'thu': 'Четверг',
             'fri': 'Пятница',
             'sat': 'Суббота',
             'sun': 'Воскресенье'
             }
teacher_times = ['8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
client_times = ['1-2', '3-5', '6-8', '9-10']


def create_timetable(timerecords):
    timetable = {dow: {} for dow in week_days.keys()}
    for t in timerecords:
        timetable[t.dow].update({t.time: t.value})

    return timetable


if __name__ == "__main__":
    pass
