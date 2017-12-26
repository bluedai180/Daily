from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=50)
    pwd = models.CharField(max_length=50)
    email = models.EmailField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    permission = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class AppDaily(models.Model):
    project = models.CharField(max_length=200)
    work_type = models.CharField(max_length=50)
    bugid = models.CharField(max_length=50)
    describe = models.CharField(max_length=200)
    priority = models.CharField(max_length=50)
    reopen = models.BooleanField()
    reopen_reason = models.CharField(max_length=200)
    solution = models.CharField(max_length=50)
    solution_reason = models.CharField(max_length=200)
    person = models.CharField(max_length=50)
    date = models.DateTimeField()
    remake = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.describe
