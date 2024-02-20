from django.contrib import admin
from .models import Racer, Group, LapTime, SortedLapTime

admin.site.register(Racer)
admin.site.register(Group)
admin.site.register(LapTime)
admin.site.register(SortedLapTime)