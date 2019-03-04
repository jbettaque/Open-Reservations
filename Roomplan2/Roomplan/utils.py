import datetime


def daterange(start_date, end_date):
    end_date = end_date + datetime.timedelta(days=1)
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def first_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead == 0:
        return d
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def first_in_month(d):
    if d.day == 1:
        return d
    return d.replace(month=d.month+1)
