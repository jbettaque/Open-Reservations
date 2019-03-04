from django.contrib import admin
from .models import Object, ObjectCategory, Organisation, Reservation, ReservationType, Quantifier

admin.site.register(Object)
admin.site.register(ObjectCategory)
admin.site.register(Organisation)
admin.site.register(Reservation)
admin.site.register(ReservationType)
admin.site.register(Quantifier)