from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    bio = models.TextField(max_length=160, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class User(models.Model):
    # ... existing fields ...

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
from django.contrib.auth.models import User
# Create your models here.
class Topic(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Movie(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)
    particpants=models.ManyToManyField(User,related_name='participants', blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return self.name

class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(Movie, on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:20]



class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    acting = models.IntegerField(default=0)
    plot = models.IntegerField(default=0)
    cinematography = models.IntegerField(default=0)
    theme = models.IntegerField(default=0)
    dialogue = models.IntegerField(default=0)
    characters = models.IntegerField(default=0)
    overall = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.movie.name} - {self.user.username}"