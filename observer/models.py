from django.db import models

class UserTypes(models.Model):
    code = models.CharField(max_length=20)
    committee = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.code


class Location(models.Model):
    name = models.CharField(max_length=200)
    last_usage_updated = models.DateField(auto_now_add=True)
    usage = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Agency(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, default="")
    type = models.CharField(max_length=50)  # either EXEC or APPROV
    description = models.TextField()
    last_usage_updated = models.DateField(auto_now_add=True)
    budget_used = models.IntegerField(default=0)
    usage = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username + " " + str(self.username)


class Project_Core(models.Model):
    name = models.CharField(max_length=200)
    project_code = models.CharField(max_length=50)
    locations = models.ManyToManyField(Location)
    executing_agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    expected_cost = models.IntegerField()
    timespan = models.IntegerField()  # years
    goal = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    feedback = models.CharField(max_length=200)
    project_core = models.ForeignKey(Project_Core, on_delete=models.CASCADE)


class Approved_Project(models.Model):
    project = models.ForeignKey(Project_Core, on_delete=models.CASCADE)
    start_date = models.DateField()
    actual_cost = models.IntegerField()

    def __str__(self):
        return self.project.name

    @property
    def completion(self):
        return self.component_set.aggregate(models.Avg('completion'))['completion__avg']


class Proposed_Project(models.Model):
    project = models.ForeignKey(Project_Core, on_delete=models.CASCADE)
    proposed_date = models.DateField()

    def __str__(self):
        return self.project.name


class Component(models.Model):
    project = models.ForeignKey(Project_Core, on_delete=models.CASCADE)
    executing_agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    component_id = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    dependancy = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    budget_ratio = models.FloatField()
    completion = models.FloatField(default = 0) # only meaningful for component of approved set

    def __str__(self):
        return self.component_id


class Agency_Constraint(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    max_limit = models.IntegerField()

    def __str__(self):
        return self.agency.name + " - " + str(self.max_limit)


class Location_Constraint(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    max_limit = models.IntegerField()

    def __str__(self):
        return self.location.name + " - " + str(self.max_limit)


class Yearly_Funding_Constraint(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    max_funding = models.IntegerField()

    def __str__(self):
        return self.agency.name + " - " + str(self.max_funding) + "$"
