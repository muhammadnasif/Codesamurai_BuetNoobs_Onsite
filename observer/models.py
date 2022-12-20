from django.db import models

# Create your models here.

# class Agency(models.Model):
#     name = models.CharField(max_length = 200)

#     def __str__(self):
#         return self.name

# class Project(models.Model):
#     name = models.CharField(max_length = 200)
#     category = models.CharField(max_length = 50)
#     description = models.TextField()
#     start_time = models.DateField()
#     completion_time = models.DateField()
#     total_budget = models.IntegerField()
#     completion_percentage = models.FloatField()
#     affiliated_agencies = models.ManyToManyField(Agency)

#     def __str__(self):
#         return self.name

# class Location(models.Model):
#     longitude = models.FloatField()
#     latitude = models.FloatField()
#     project = models.ForeignKey(Project, on_delete = models.CASCADE)
    
#     def __str__(self):
#         return f'({self.longitude}, {self.latitude})'

# class Issue(models.Model):
#     location = models.ForeignKey(Location, on_delete = models.CASCADE)
#     description = models.TextField()
#     sender = models.CharField(max_length = 200, default="Nasif")   # TODO make user?

#     def __str__(self):
#         return self.description


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Agency(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Project_Core(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    executing_agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    project_code = models.CharField(max_length=50)
    expected_cost = models.IntegerField()
    timespan = models.IntegerField() # years
    goal = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Approved_Project(models.Model):
    project = models.ForeignKey(Project_Core, on_delete=models.CASCADE)
    start_date = models.DateField()
    completion = models.FloatField()
    actual_cost = models.IntegerField()

    def __str__(self):
        return self.project.name

class Proposed_Project(models.Model):
    project = models.ForeignKey(Project_Core, on_delete=models.CASCADE)
    proposed_date = models.DateField()

    def __str__(self):
        return self.project.name
