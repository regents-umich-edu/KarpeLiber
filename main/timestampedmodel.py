from django.db import models


class TimeStampedModel(models.Model):
    # null allowed to accommodate import of historical data without values
    addedTime = models.DateTimeField(auto_now_add=True, null=True)
    updatedTime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
