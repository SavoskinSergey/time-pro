from django.db import models
from django.utils.translation import gettext_lazy as _
from core.abstract.models import AbstractModel, AbstractManager


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/employee_<id>/<filename>
    return f'employee_{instance.public_id}/{filename}'


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('department')
        verbose_name_plural = _('departments')

    def __str__(self):
        return self.name


class EmployeeManager(AbstractManager):
    pass


class Employee(AbstractModel):
    employee = models.CharField(db_index=True, max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(db_index=True, unique=True)
    # department = models.CharField(max_length=100, null=True, blank=True)
    # #     related_name='employees)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='employees',
        verbose_name=_('department'),
        )
    title = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    avatar = models.ImageField(
                    null=True, blank=True, upload_to=user_directory_path
                    )
    note = models.TextField(null=True, blank=True)

    # events_subscribed = models.ManyToManyField(
    #     'core_event.Event',
    #     related_name='subscribed_by'
    # )

    objects = EmployeeManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    # def subscribe(self, event):
    #     """Subscribe 'event' if it hasn't been done yet"""
    #     return self.events_subscribed.add(event)

    # def remove_subscribe(self, event):
    #     """Remove a subscribe from a 'event'"""
    #     return self.events_subscribed.remove(event)

    # def has_subscribed(self, event):
    #     """Return True if the user has subscribed a 'event'; else False"""
    #     return self.events_subscribed.filter(pk=event.pk).exists()
