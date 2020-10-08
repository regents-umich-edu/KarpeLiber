import calendar

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


class Topic(models.Model):
    class Meta:
        db_table = 'topic'

    name = models.CharField(max_length=200)
    dateAdded = models.DateField('added on date')
    dateUpdated = models.DateField('updated on date')

    def __str__(self):
        return self.name


class Item(models.Model):
    class Meta:
        db_table = 'item'

    name = models.CharField(max_length=200)
    dateAdded = models.DateField('added on date')
    dateUpdated = models.DateField('updated on date')
    topicId = models.OneToOneField(
        Topic,
        related_name='items',
        on_delete=models.DO_NOTHING, )

    def __str__(self):
        return self.name


class ItemPage(models.Model):
    class Meta:
        db_table = 'item_page'

    itemId = models.OneToOneField(
        Item,
        related_name='itemPages',
        on_delete=models.DO_NOTHING, )
    volumeId = models.OneToOneField(
        Volume,
        related_name='volumeItemPages',
        on_delete=models.DO_NOTHING, )
    page = models.IntegerField('page number')
    date = models.DateField('date of mention')
    year = models.IntegerField('year of mention')
    month = models.IntegerField(
        'month of mention',
        choices=models.IntegerChoices(
            'month',
            calendar.month_abbr[1:]).choices,
        null=True, )


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

    typeId = models.OneToOneField(
        NoteType,
        related_name='topicNotes',
        on_delete=models.DO_NOTHING, )
    topicId = models.OneToOneField(
        Topic,
        related_name='noteTopic',
        on_delete=models.DO_NOTHING, )
    text = models.CharField(max_length=500)
    relatedTopicId = models.OneToOneField(
        Topic,
        related_name='topicNoteRelatedTopic',
        on_delete=models.DO_NOTHING, )

    def __str__(self):
        return self.text


class ItemNote(models.Model):
    class Meta:
        db_table = 'item_note'

    typeId = models.OneToOneField(
        NoteType,
        related_name='itemNotes',
        on_delete=models.DO_NOTHING, )
    itemId = models.OneToOneField(
        Item,
        related_name='noteItem',
        on_delete=models.DO_NOTHING, )
    text = models.CharField(max_length=500)
    relatedTopicId = models.OneToOneField(
        Topic,
        related_name='itemNoteRelatedTopic',
        on_delete=models.DO_NOTHING, )

    def __str__(self):
        return self.text


class PageMapping(models.Model):
    class Meta:
        db_table = 'page_mapping'

    volumeId = models.OneToOneField(
        Volume,
        related_name='volume_page_mapping',
        on_delete=models.DO_NOTHING, )
    libraryNum = models.CharField('library call number', max_length=200)
    # A few page numbers may be Roman numerals, have letter suffix, etc.
    page = models.CharField('page number', max_length=20)
    imageNumber = models.IntegerField('image number')
    confidence = models.IntegerField('scan quality confidence')
    pageType = models.CharField('page content type', max_length=20)
