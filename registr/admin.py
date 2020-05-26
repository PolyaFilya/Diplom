from django.contrib import admin

from .models import Event, User, State

admin.site.register(Event)
admin.site.register(User)
admin.site.register(State)