from datetime import datetime

from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

from Roomplan.models import TestModel
nowstring = datetime.now().strftime("DD.MM.YYYY")

tooltips = {
    "today": 'Heute',
    "clear": 'Löschen',
    "close": 'Schließen',
    "selectMonth": 'Monat auswählen',
    "prevMonth": 'letzter Monat',
    "nextMonth": 'nächster Monat',
    "selectYear": 'nächstes Jahr',
    "prevYear": 'letztes Jahr',
    "nextYear": 'nächstes Jahr',
}


class WeekViewForm(forms.Form):
    anfang = forms.DateTimeField(
        input_formats=['%d.%m.%Y'],
        widget=DatePickerInput(options={
            "format": "DD.MM.YYYY",
            "locale": "de",
            "tooltips": tooltips
        }).start_of('view dates'),
    )
    ende = forms.DateTimeField(
        input_formats=['%d.%m.%Y'],
        widget=DatePickerInput(options={
            "format": "DD.MM.YYYY",
            "locale": "de",
        }).end_of('view dates')
    )


class CreateTimesForm(forms.Form):
    start_date = forms.DateTimeField(
        input_formats=['%d.%m.%Y'],
        widget=DatePickerInput(options={
            "format": "DD.MM.YYYY",
            "locale": "de",
            "tooltips": tooltips
        }).start_of('create dates'),
    )

    end_date = forms.DateTimeField(
        input_formats=['%d.%m.%Y'],
        widget=DatePickerInput(options={
            "format": "DD.MM.YYYY",
            "locale": "de",
            "tooltips": tooltips,
        }).start_of('create dates'),
    )

    start_time = forms.TimeField(
        widget=TimePickerInput(options={
            "format": "HH:mm",
            "locale": "de",
            "tooltips": tooltips
        }).start_of('create times'),
    )

    end_time = forms.TimeField(
        widget=TimePickerInput(options={
            "format": "HH:mm",
            "locale": "de",
            "tooltips": tooltips
        }).start_of('create times'),
    )
