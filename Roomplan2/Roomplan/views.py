from django.http import HttpResponse
from django.shortcuts import render
from .models import Reservation, Object, ObjectCategory, ReservationType, Quantifier
from .forms import WeekViewForm, CreateTimesForm
from .utils import daterange, first_weekday
import locale
import datetime


def week(request):
    start_date = first_weekday(datetime.datetime.now(), 0) - datetime.timedelta(days=7)
    end_date = start_date + datetime.timedelta(days=6)

    if request.method == "GET":
        f = WeekViewForm(request.GET)
        if f.is_valid():
            start_date = f.cleaned_data["anfang"]
            end_date = f.cleaned_data["ende"]
    else:
        f = WeekViewForm(request.GET)

    objects = []
    for category in ObjectCategory.objects.all():
        for object in category.object_set.all():
            objects.append(object)

    reservations = Reservation.objects.filter(organisation__reservation__start_date__lte=end_date)
    reservations = Reservation.objects.all()
    print(reservations)

    days = []
    # TODO CHANGE FOR LINUX IN PRODUCTION!
    locale.setlocale(locale.LC_ALL, 'deu_deu')
    for day in daterange(start_date, end_date):
        days.append({'date': day, 'string': day.strftime('%A, %d. %m')})

    results = []
    for day in days:
        reservationlist = []

        for reservation in reservations:
            if reservation.isReservated(day['date']):
                reservationlist.append(reservation)

        results.append({'date': day, 'reservationlist': reservationlist, 'reservationlist_len': len(reservationlist)})
        reservationlist = []

    return render(request, 'week.html', {
        'form': f,
        'days': days,
        'objects': objects,
        'results': results,
    })


def create(request):
    create_dates_form = CreateTimesForm()

    if request.method == 'POST':
        post = request.POST

        object = Object.objects.filter(id=post['object']).first()

        template = ""
        start_date = ""
        end_date = ""
        start_time = ""
        end_time = ""
        name = ""
        notes = ""
        materials = ""
        color = ""
        approved = True

        if "templateRadios" in post.keys():
            template = post["templateRadios"]

        if "start_date" in post.keys():
            start_date = post["start_date"]
        if "end_date" in post.keys():
            end_date = post["end_date"]

        if "start_time" in post.keys():
            start_time = post["start_time"]
        if "end_time" in post.keys():
            end_time = post["end_time"]

        if "name" in post.keys():
            name = post["name"]

        if "notes" in post.keys():
            notes = post["notes"]
        if "materials" in post.keys():
            materials = post["materials"]

        if "colorRadios" in post.keys():
            color = post["colorRadios"]

        print(""
              "template: " + template +
              "\nname: " + name +
              "\nstart_date: " + start_date +
              "\nend_date: " + end_date +
              "\nstart_time: " + start_time +
              "\nend_time: " + end_time +
              "\nnotes: " + notes +
              "\nmaterials: " + materials +
              "")

        # start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y")
        # end_date = datetime.datetime.strptime(end_date, "%d.%m.%Y")

        start_time = datetime.datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.datetime.strptime(end_time, "%H:%M").time()

        # einmalig
        if template == "0":
            if name != "":
                start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y")
                end_date = start_date

                quant = Quantifier(name="single", value="0")
                quant.save()
                resType = ReservationType(name=name, smallQuantifier=quant, bigQuantifier=quant)
                resType.save()

                reservation = Reservation(name=name, reservedObject=object, user=request.user, reservationType=resType,
                                          notes=notes, color=color, materials=materials, approved=approved,
                                          start_date=start_date, end_date=end_date, start_time=start_time,
                                          end_time=end_time)

                reservation.save()

        # jeder x (wochentag) alle x wochen
        if template == "1":
            if name != "":
                start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y")
                end_date = datetime.datetime.strptime(end_date, "%d.%m.%Y")

                number = post["template1numbers"]
                weekday = post["template1weekdays"]

                smallQuant = Quantifier(name="number", value=weekday)
                smallQuant.save()
                bigQuant = Quantifier(name="x_weeks", value=number)
                bigQuant.save()

                resType = ReservationType(name=name, smallQuantifier=smallQuant, bigQuantifier=bigQuant)
                resType.save()

                reservation = Reservation(name=name, reservedObject=object, user=request.user, reservationType=resType,
                                          notes=notes, color=color, materials=materials, approved=approved,
                                          start_date=start_date, end_date=end_date, start_time=start_time,
                                          end_time=end_time)

                reservation.save()


        # jeder x (wochentag)
        if template == "2":
            if name != "":
                start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y")
                end_date = datetime.datetime.strptime(end_date, "%d.%m.%Y")

                weekday = post["template2weekdays"]

                smallQuant = Quantifier(name="number", value=weekday)
                smallQuant.save()
                bigQuant = Quantifier(name="x_weeks", value=1)
                bigQuant.save()

                resType = ReservationType(name=name, smallQuantifier=smallQuant, bigQuantifier=bigQuant)
                resType.save()

                reservation = Reservation(name=name, reservedObject=object, user=request.user, reservationType=resType,
                                          notes=notes, color=color, materials=materials, approved=approved,
                                          start_date=start_date, end_date=end_date, start_time=start_time,
                                          end_time=end_time)

                reservation.save()

        if template == "3":
            if name != "":
                start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y")
                end_date = datetime.datetime.strptime(end_date, "%d.%m.%Y")

                if "monthday" in post.keys():
                    monthday = post["monthday"]
                else:
                    monthday = 1

                smallQuant = Quantifier(name="number", value=monthday)
                smallQuant.save()
                bigQuant = Quantifier(name="in_month", value=0)
                bigQuant.save()

                resType = ReservationType(name=name, smallQuantifier=smallQuant, bigQuantifier=bigQuant)
                resType.save()

                reservation = Reservation(name=name, reservedObject=object, user=request.user, reservationType=resType,
                                          notes=notes, color=color, materials=materials, approved=approved,
                                          start_date=start_date, end_date=end_date, start_time=start_time,
                                          end_time=end_time)

                reservation.save()

    weekdays = {
        1: 'Montag',
        2: 'Dienstag',
        3: 'Mittwoch',
        4: 'Donnerstag',
        5: 'Freitag',
        6: 'Samstag',
        7: 'Sonntag',
    }

    colors = [
        'primary',
        'info',
        'danger',
        'success',
        'warning',
        'dark'
    ]

    objects = Object.objects.all()

    context = {
        'weekdays': weekdays,
        'form': create_dates_form,
        'colors': colors,
        'objects': objects,
    }

    return render(request, 'create.html', context)
