import calendar
import datetime
import logging
from typing import Optional

from django.db import models
from django.db.models.query import QuerySet

from main import timestampedmodel

logger = logging.getLogger(__name__)


class Volume(models.Model):
    objects: models.QuerySet
    pageMappings: models.QuerySet

    class Meta:
        db_table = 'volume'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    dateBegin = models.DateField('beginning date')
    dateEnd = models.DateField('ending date')
    pages = models.BigIntegerField('total number of pages')
    available = models.BooleanField('available online', default=False)
    libraryNum = models.CharField('library call number', max_length=200)

    @property
    def url(self):
        return self.makeUrl()

    url.fget.short_description = 'Library URL for volume'

    def makeUrl(self, page: str = None) -> Optional[str]:
        '''
        Some volumes may not use PageMapping.  Those cases are detected by
        their total lack of PageMapping objects.  In those cases, return the
        page number directly.  Otherwise, if a mapping for a page wasn't
        found, but the volume has PageMapping objects, return `None`.  Those
        cases are most likely mistakes in page numbers.

        :param page:
        :return:
        '''
        # TODO: decide whether "unavailable" volumes are available to admin
        # TODO: make separate `adminUrl()` methods?
        if not self.available or not self.libraryNum:
            return None

        # TODO: get the host and base URL from app config
        volumeUrl: Optional[str] = (
            f'https://quod.lib.umich.edu/u/umregproc/{self.libraryNum}')

        if page:
            pageMaps: QuerySet = (
                self.pageMappings.filter(page=page))
            if len(pageMaps) > 1:
                logger.warning(f'Multiple mappings for volume ({self.id}), '
                               f'page ({page}).')

            pageMap: PageMapping = pageMaps.first()

            if pageMap:
                logger.debug(
                    f'{self}, {page}, {pageMap.page}, {pageMap.imageNumber}')
                volumeUrl += f'/{pageMap.imageNumber}'
            elif self.pageMappings.count() == 0:
                logger.debug(f'no pageMappings for volume {self.id}')
                volumeUrl += f'/{page}'
            else:
                logger.warning(f'Volume ({self.id}) uses PageMapping, but '
                               f"page ({page}) couldn't be found.")
                volumeUrl = None

        return volumeUrl

    def __str__(self):
        return f'{self.title}'


class Topic(timestampedmodel.TimeStampedModel):
    objects: models.QuerySet

    class Meta:
        db_table = 'topic'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    @property
    def numItems(self) -> int:
        # Item.objects.filter(topic=self).count()
        return self.items.count()

    numItems.fget.short_description = 'Number of items'

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

    id = models.AutoField(primary_key=True)
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

    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(
        Item,
        related_name='itemPages',
        on_delete=models.DO_NOTHING, )
    volume: Volume = models.ForeignKey(
        Volume,
        related_name='volumeItemPages',
        on_delete=models.DO_NOTHING,
        null=True)
    page = models.IntegerField('page number')
    date: datetime.date = models.DateField(
        'date of mention',
        null=True,
        blank=True,
        # default=datetime.date.today,
    )
    year = models.IntegerField(
        'year of mention',
        null=True,
        blank=True,
    )
    month = models.IntegerField(
        'month of mention',
        choices=models.IntegerChoices(
            'month',
            calendar.month_abbr[1:]).choices,
        null=True,
        blank=True,
    )

    @property
    def url(self):
        # TODO: get the host and base URL from app config
        if self.volume is None:
            return None
        return self.volume.makeUrl(self.page)

    url.fget.short_description = 'Library URL for volume with page'

    @property
    def dateCalc(self) -> Optional[str]:
        """
        use date if specified, otherwise make one from year/month,
        else return `None`

        :return: str "Mon YYYY" or none
        """
        if self.date:
            result = self.date.strftime('%b %Y')
        elif self.year and self.month:
            result = f'{calendar.month_abbr[self.month]} {self.year}'
        else:
            result = None

        return result

    def __str__(self):
        return (f'ItemPage {self.page} ('
                f'{self.volume if self.volume else "NO_VOLUME"}, '
                f'{self.date.strftime("%Y-%b") if self.date else "NO_DATE"})')


class NoteType(models.Model):
    class Meta:
        db_table = 'note_type'

    id = models.AutoField(primary_key=True)
    # FIXME: should these have `unique=True`?
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TopicNote(models.Model):
    class Meta:
        db_table = 'topic_note'

    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(
        NoteType,
        related_name='topicNotes',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING, )
    topic = models.ForeignKey(
        Topic,
        related_name='topicNotes',
        on_delete=models.DO_NOTHING, )
    text = models.CharField(
        max_length=500,
        blank=True,
        null=True, )
    referencedTopic = models.ForeignKey(
        Topic,
        related_name='topicNoteReferences',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING, )

    def __str__(self):
        referencedTopicName = self.referencedTopic.name \
            if self.referencedTopic else None
        # if self.referencedTopic else '[No referenced topic]'
        noteParts = ', '.join(
            filter(None, (str(self.id), self.text, referencedTopicName)))
        return f'{self.type}: {noteParts}'


class ItemNote(models.Model):
    class Meta:
        db_table = 'item_note'

    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(
        NoteType,
        related_name='itemNotes',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING, )
    item = models.ForeignKey(
        Item,
        related_name='itemNotes',
        on_delete=models.DO_NOTHING, )
    text = models.CharField(
        max_length=500,
        blank=True,
        null=True, )
    referencedTopic = models.ForeignKey(
        Topic,
        related_name='itemNoteReferences',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING, )

    def __str__(self):
        return f'{self.type}: {self.text}'


class PageMapping(models.Model):
    class Meta:
        db_table = 'page_mapping'

    id = models.AutoField(primary_key=True)
    volume = models.ForeignKey(
        Volume,
        related_name='pageMappings',
        on_delete=models.DO_NOTHING, )
    # A few page numbers may be Roman numerals, have letter suffix, etc.
    page = models.CharField('page number', max_length=20)
    imageNumber = models.IntegerField('image number')
    confidence = models.IntegerField('scan quality confidence')
    pageType = models.CharField('page content type', max_length=20)
