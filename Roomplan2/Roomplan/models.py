from django.db import models
from django.contrib.auth.models import User
from .utils import daterange, first_weekday, first_in_month
import datetime
from dateutil import relativedelta


class TestModel(models.Model):
    date = models.DateTimeField()


class ObjectCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ObjectCategory, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return self.name


class Organisation(models.Model):
    name = models.CharField(max_length=100)

    color = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    person_name = models.CharField(max_length=100, null=True, blank=True)
    person_contact = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Quantifier(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class ReservationType(models.Model):
    name = models.CharField(max_length=100)

    smallQuantifier = models.ForeignKey(Quantifier, on_delete=models.CASCADE, related_name="smallQuantifier")
    bigQuantifier = models.ForeignKey(Quantifier, on_delete=models.CASCADE, related_name="bigQuantifier")

    def __str__(self):
        return self.name


class Reservation(models.Model):
    name = models.CharField(max_length=200)
    reservedObject = models.ForeignKey(Object, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservationType = models.ForeignKey(ReservationType, on_delete=models.CASCADE)

    notes = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    materials = models.TextField(null=True, blank=True)

    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, blank=True)

    approved = models.BooleanField(default=False)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    def text_islight(self):
        list = ["primary", "success", "danger", "info", "dark"]

        if self.color in list:
            return True
        return False

    def __str__(self):
        return self.name

    def start_time_string(self):
        return self.start_time.strftime('%H:%M')

    def end_time_string(self):
        return self.end_time.strftime('%H:%M')

    def isReservated(self, date):
        if self.reservationType.smallQuantifier.name == "single" or self.reservationType.bigQuantifier.name == "single":
            if self.start_date.date() == date.date():
                return True

        if self.reservationType.smallQuantifier.name == "number":
            if self.reservationType.bigQuantifier.name == "x_weeks":
                # every number in x weeks (every 2. day in 2 weeks / every 2. tuesday)
                number = self.reservationType.smallQuantifier.value
                x = self.reservationType.bigQuantifier.value

                # start with first monday
                current_date = first_weekday(self.start_date, 0)
                weekcounter = 0

                while current_date <= self.end_date:
                    if weekcounter % int(x) == 0:
                        if date.date() == current_date.date() + datetime.timedelta(days=float(int(number) - 1)):
                            return True

                    current_date += datetime.timedelta(days=7)
                    weekcounter += 1

            if self.reservationType.bigQuantifier.name == "in_month":

                # every number every month (every 01. in every month)
                number = self.reservationType.smallQuantifier.value

                if self.start_date < date < self.end_date:
                    if date.day == int(number):
                        return True

            if self.reservationType.bigQuantifier.name == "in_week":
                # every number every week (every 2. day every week / every tuesday)
                number = self.reservationType.smallQuantifier.value

                # start with first monday
                current_date = first_weekday(self.start_date, 0)

                while current_date <= self.end_date:
                    if date.date() == current_date.date() + datetime.timedelta(days=float(int(number) - 1)):
                        return True

                    current_date += datetime.timedelta(days=7)

        if self.reservationType.smallQuantifier.name == "weekday":
            # every x. monday every month
            if self.reservationType.bigQuantifier.name == "in_month":

                # 0 is monday 6 is sunday
                weekday = int(self.reservationType.smallQuantifier.value) - 1

                x = int(self.reservationType.bigQuantifier.value)

                current_date = first_weekday(self.start_date, weekday)
                weekcounter = 0

                while current_date <= self.end_date:
                    if weekcounter % int(x) == 0:
                        if current_date.date() == date.date():
                            return True

                    current_date += datetime.timedelta(days=7)
                    weekcounter += 1

        return False


