from django.db import models
from core.account.models import User


class Question(models.Model):
    name = models.TextField()
    body = models.TextField()
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_edited = models.DateTimeField(
        null=True
    )
    creator = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='questions'
            )

    def __str__(self):
        return "{} - {}".format(self.creator.username, self.name)
