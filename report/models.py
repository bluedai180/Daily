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

    def is_manager(self):
        if self.team.name == "director":
            return True
        return False


class Project(models.Model):
    name = models.CharField(max_length=200, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SoftDaily(models.Model):
    project = models.CharField(max_length=200, blank=True, null=True)
    work_type = models.CharField(max_length=50, blank=True, null=True)
    bugid = models.CharField(max_length=50, blank=True, null=True)
    describe = models.CharField(max_length=200, blank=True, null=True)
    priority = models.CharField(max_length=50, blank=True, null=True)
    reopen = models.CharField(max_length=50, blank=True, null=True)
    reopen_reason = models.CharField(max_length=200, blank=True, null=True)
    solution = models.CharField(max_length=50, blank=True, null=True)
    solution_reason = models.CharField(max_length=200, blank=True, null=True)
    person = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    remake = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.describe

    class Meta:
        abstract = True


class AppDaily(SoftDaily):
    pass


class FrameworkDaily(SoftDaily):
    pass


class DriverDaily(SoftDaily):
    pass


class ProtocolDaily(SoftDaily):
    pass


class SPMDaily(SoftDaily):
    pass


class App3Daily(SoftDaily):
    pass


class SoftWeekly(models.Model):
    project = models.CharField(max_length=200, blank=True, null=True)
    info = models.CharField(max_length=2000, blank=True, null=True)
    time = models.CharField(max_length=200, blank=True, null=True)
    next_week = models.CharField(max_length=2000, blank=True, null=True)
    difficult = models.CharField(max_length=2000, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    email = models.EmailField()
    total = models.BooleanField(default=False)

    def __str__(self):
        return self.project

    class Meta:
        abstract = True


class AppWeekly(SoftWeekly):
    pass


class ProtocolWeekly(SoftWeekly):
    pass


class FrameworkWeekly(SoftWeekly):
    pass


class DriverWeekly(SoftWeekly):
    pass


class SPMWeekly(SoftWeekly):
    pass


class App3Weekly(SoftWeekly):
    pass
