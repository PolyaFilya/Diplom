import datetime

from django.db import models
from django.utils import timezone
from datetime import datetime

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    event_date = models.DateTimeField(auto_now=False)
    def __str__(self):
        return self.event_name

class User(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=7)
    email = models.EmailField(max_length=150)
    age = models.CharField(max_length=3)
    def __str__(self):
        return self.first_name

class State(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_state = models.CharField(max_length=50)    
    reg_time = models.DateTimeField(auto_now_add = True)    
    def __str__(self):
        return self.name_state

class QR(models.Model):
    file = models.ImageField(upload_to = 'qrs')
