from django.db import models


class TimeStampedModel(models.Model):
    addedTime = models.DateTimeField(auto_now_add=True)
    updatedTime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
