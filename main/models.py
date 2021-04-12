import calendar
import datetime

from django.db import models

from main import timestampedmodel


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
        return f'https://quod.lib.umich.edu/' \
               f'u/umregproc/acw7513.{self.title}.001'

    url.fget.short_description = 'Library URL'

    def __str__(self):
        return f'{self.title}'


class Topic(timestampedmodel.TimeStampedModel):
    objects: models.QuerySet

    class Meta:
        db_table = 'topic'

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.name}'


class Item(timestampedmodel.TimeStampedModel):
    objects: models.QuerySet

    class Meta:
        db_table = 'item'

        # FIXME: requires cleaning up old data, but no time for that now
        # FIXME: reinstate this after old data is in production
        # constraints = (
        #     models.UniqueConstraint(fields=('name', 'topic',),
        #                             name='topic_item'),
        # )

    name = models.CharField(max_length=400)
    topic = models.ForeignKey(
        Topic,
        related_name='items',
        on_delete=models.DO_NOTHING, )

    def __str__(self):
        return f'{self.name}'


class ItemPage(models.Model):
    objects: models.QuerySet

    class Meta:
        db_table = 'item_page'

    item = models.ForeignKey(
        Item,
        related_name='itemPages',
        on_delete=models.DO_NOTHING, )
    # volume = models.ForeignKey(
    #     Volume,
    #     related_name='volumeItemPages',
    #     on_delete=models.DO_NOTHING,
    #     null=True)
    page = models.IntegerField('page number')
    date: datetime.date = models.DateField(
        'date of mention',
        null=True,
        # default=datetime.date.today,
    )

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
        """
        use date if specified, otherwise make one from year/month

        if no year/month, return year only
        else return None

        :return:
        """
        if self.date:
            result = self.date.strftime('%B, %Y')
        elif self.year and self.month:
            result = f'{calendar.month_name[self.month]}, {self.year}'
        elif self.year:
            result = self.year
        else:
            result = None

        return result

    def __str__(self):
        return f'Page: {self.page} {self.date}'


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
    text = models.CharField(
        max_length=500,
        blank=True,
        null=True, )
    referencedTopic = models.ForeignKey(
        Topic,
        related_name='topicNoteReferencedTopic',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING, )

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
    text = models.CharField(
        max_length=500,
        blank=True,
        null=True, )
    referencedTopic = models.ForeignKey(
        Topic,
        related_name='itemNoteReferencedTopic',
        blank=True,
        null=True,
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
