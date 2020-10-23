import calendar
import datetime

from django.db import models


class Volume(models.Model):
    objects: models.QuerySet

    class Meta:
        db_table = 'volume'

    title = models.CharField(max_length=200)
    dateBegin = models.DateField('beginning date')
    dateEnd = models.DateField('ending date')
    pages = models.BigIntegerField('number of pages')
    available = models.BooleanField('available online', default=False)

    @property
    def url(self):
        # TODO: get the host and base URL from app config
        return f'https://quod.lib.umich.edu/u/umregproc/acw7513.{self.title}.001'

    url.fget.short_description = 'Library URL'

    def __str__(self):
        return f'{self.title}'


class Topic(models.Model):
    objects: models.QuerySet

    class Meta:
        db_table = 'topic'

    name = models.CharField(max_length=200, unique=True)
    dateAdded = models.DateField('added on date', default=datetime.date.today)
    dateUpdated = models.DateField('updated on date',
                                   default=datetime.date.today)

    def __str__(self):
        return f'{self.name} - {self.dateAdded} - {self.dateUpdated}'


class Item(models.Model):
    objects: models.QuerySet

    class Meta:
        db_table = 'item'
        constraints = (
            models.UniqueConstraint(fields=('name', 'topic',),
                                    name='topic_item'),
        )

    name = models.CharField(max_length=200)
    topic = models.ForeignKey(
        Topic,
        related_name='items',
        on_delete=models.DO_NOTHING, )
    dateAdded = models.DateField('added on date', default=datetime.date.today)
    dateUpdated = models.DateField('updated on date',
                                   default=datetime.date.today)

    def __str__(self):
        # return f'{self.name} ({self.topic.name})'
        return f'{self.name}'


class ItemPage(models.Model):
    objects: models.QuerySet

    class Meta:
        db_table = 'item_page'

    item = models.ForeignKey(
        Item,
        related_name='itemPages',
        on_delete=models.DO_NOTHING, )
    volume = models.ForeignKey(
        Volume,
        related_name='volumeItemPages',
        on_delete=models.DO_NOTHING,
        null=True)
    page = models.IntegerField('page number')
    date = models.DateField(
        'date of mention',
        null=True, )
    year = models.IntegerField('year of mention')
    month = models.IntegerField(
        'month of mention',
        choices=models.IntegerChoices(
            'month',
            calendar.month_abbr[1:]).choices,
        null=True, )

    # TODO: calculate which volume based on date
    # @property
    # def volumeCalc(self):
    #     return Volume.objects.filter()

    @property
    def dateCalc(self):
        return self.date if self.date is not None \
            else datetime.datetime(
            int(self.year if self.year else 0),
            int(self.month if self.month else 0),
            1)
        # else f'{int(self.year if self.year else 0)}, {self.month}, 1'

    def __str__(self):
        return f'Page: {self.page} {self.volume}'


class NoteType(models.Model):
    class Meta:
        db_table = 'note_type'

    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TopicNote(models.Model):
    class Meta:
        db_table = 'topic_note'

    type = models.ForeignKey(
        NoteType,
        related_name='topicNotes',
        on_delete=models.DO_NOTHING, )
    topic = models.ForeignKey(
        Topic,
        related_name='noteTopic',
        on_delete=models.DO_NOTHING, )
    text = models.CharField(max_length=500)
    referencedTopic = models.ForeignKey(
        Topic,
        related_name='topicNoteReferencedTopic',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return f'{self.type}: {self.text}'


class ItemNote(models.Model):
    class Meta:
        db_table = 'item_note'

    type = models.ForeignKey(
        NoteType,
        related_name='itemNotes',
        on_delete=models.DO_NOTHING, )
    item = models.ForeignKey(
        Item,
        related_name='noteItem',
        on_delete=models.DO_NOTHING, )
    text = models.CharField(max_length=500)
    referencedTopic = models.ForeignKey(
        Topic,
        related_name='itemNoteReferencedTopic',
        on_delete=models.DO_NOTHING, )

    def __str__(self):
        return f'{self.type}: {self.text}'


class PageMapping(models.Model):
    class Meta:
        db_table = 'page_mapping'

    volume = models.ForeignKey(
        Volume,
        related_name='volume_page_mapping',
        on_delete=models.DO_NOTHING, )
    libraryNum = models.CharField('library call number', max_length=200)
    # A few page numbers may be Roman numerals, have letter suffix, etc.
    page = models.CharField('page number', max_length=20)
    imageNumber = models.IntegerField('image number')
    confidence = models.IntegerField('scan quality confidence')
    pageType = models.CharField('page content type', max_length=20)
