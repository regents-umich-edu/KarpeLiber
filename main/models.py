from django.db import models


class Volume(models.Model):
    class Meta:
        db_table = 'volume'

    title = models.CharField(max_length=200)
    dateBegin = models.DateField('beginning date')
    dateEnd = models.DateField('ending date')
    pages = models.BigIntegerField('number of pages')
    available = models.BooleanField('available online', default=False)

    def __str__(self):
        return self.title
