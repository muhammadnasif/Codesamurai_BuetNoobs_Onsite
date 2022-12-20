from django.db import models

# Create your models here.

class Agency(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length = 200)
    category = models.CharField(max_length = 50)
    description = models.TextField()
    start_time = models.DateField()
    completion_time = models.DateField()
    total_budget = models.IntegerField()
    completion_percentage = models.FloatField()
    affiliated_agencies = models.ManyToManyField(Agency)

    def __str__(self):
        return self.name

class Location(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    
    def __str__(self):
        return f'({self.longitude}, {self.latitude})'

class Issue(models.Model):
    location = models.ForeignKey(Location, on_delete = models.CASCADE)
    description = models.TextField()
    sender = models.CharField(max_length = 200, default="Nasif")   # TODO make user?

    def __str__(self):
        return self.description


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
