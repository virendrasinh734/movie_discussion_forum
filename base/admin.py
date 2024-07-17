from django.contrib import admin

# Register your models here.
from .models import Movie, Message,Topic
admin.site.register(Movie)
admin.site.register(Message)
admin.site.register(Topic)

