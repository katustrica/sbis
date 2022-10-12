from django.contrib import admin

from django.contrib import admin
from Hotel.models import EventBRS, ActiveIntervalsBRS, Booking

admin.site.register(EventBRS)
admin.site.register(ActiveIntervalsBRS)
admin.site.register(Booking)
