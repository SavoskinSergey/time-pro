from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Task(MPTTModel):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children'
        )
    amount = models.DecimalField(max_digits=10, decimal_places=1)

    class MPTTMeta:
        order_insertion_by = ['title']

    # class Meta:
    #     ordering =  ['level', 'title',]

    def __str__(self):
        return self.title
