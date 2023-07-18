from datetime import date
from django.db import models
from core.abstract.models import AbstractModel, AbstractManager
from core.account.models import User
from core.employee.models import Employee
from django.core.validators import MaxValueValidator, MinValueValidator


class ProjectManager(AbstractManager):
    pass


class Project(AbstractModel):
    account = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='projects',
            default=1
            )
    title = models.CharField(max_length=255)
    counterparty = models.CharField(max_length=50)
    stage = models.CharField(max_length=50)
    budget = models.DecimalField(max_digits=10, decimal_places=1)
    responsible = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    note = models.TextField(null=True, blank=True)

    members = models.ManyToManyField(
        'core_employee.Employee',
        related_name='members_by'
    )

    objects = ProjectManager()

    def __str__(self):
        return f'{self.counterparty}  - {self.stage}'

    # def subscribe(self, event):
    #     """Subscribe 'event' if it hasn't been done yet"""
    #     return self.events_subscribed.add(event)

    # def remove_subscribe(self, event):
    #     """Remove a subscribe from a 'event'"""
    #     return self.events_subscribed.remove(event)

    # def has_subscribed(self, event):
    #     """Return True if the user has subscribed a 'event'; else False"""
    #     return self.events_subscribed.filter(pk=event.pk).exists()
    def total_charged(self, event):
        """Return True if the user has subscribed a 'event'; else False"""
        return self.events_subscribed.filter(pk=event.pk).exists()


class TimeEntryManager(AbstractManager):
    pass


class TimeEntry(AbstractModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_time = models.DateField()
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    week = models.PositiveSmallIntegerField(blank=True, null=True)
    time_spent = models.DecimalField(
            max_digits=4,
            decimal_places=1,
            validators=[
                MaxValueValidator(24),
                MinValueValidator(0)]
    )
    comment = models.TextField(null=True, blank=True)

    objects = TimeEntryManager()

    def __str__(self):
        return f'{self.employee}  - {self.project}'

    def save(self, *args, **kwargs):
        self.year = self.start_time.year
        day_of_year = (
            self.start_time.toordinal() 
            - date(self.year, 1, 1).toordinal() + 1
        )
        day_of_week = self.start_time.isoweekday()
        if day_of_week == 7:
            day_of_week = 0  # воскресенье
        ordinal_number = (
            (day_of_year - day_of_week) // 7
            + (1 if day_of_week != 7 else 0)
        )
        self.week = ordinal_number
        super().save(*args, **kwargs)
