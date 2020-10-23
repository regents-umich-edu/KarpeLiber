import calendar
import io
import logging

import pandas as pd
from django.contrib import messages
from django.contrib.admin import site, register, ModelAdmin, \
    TabularInline
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import forms
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.html import format_html

from main import models
# TODO: learn about django_extensions.logging
# from django_extensions import logging
# from main.reverseadmin import ReverseModelAdmin
from main.models import Topic, Item, ItemPage

logger = logging.getLogger(__name__)


class KarpeLiberTabularInline(TabularInline):
    extra = 0  # don't show "add another" rows by default
    show_change_link = True


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()
    csv_file.label = 'CSV file'
    # csv_file.help_text = 'list of column names or something helpful'
    csv_file.required = True


@register(models.TopicNote)
class TopicNoteAdmin(ModelAdmin):
    change_list_template = 'entities/TopicNote_change_list.html'

    def get_urls(self):
        return [
                   path('import-csv/', self.import_csv),
               ] + super().get_urls()

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file: InMemoryUploadedFile = request.FILES['csv_file']
            logger.debug(csv_file)
            logger.debug(type(csv_file))

            # TODO: use content_type for validation
            logger.debug(csv_file.content_type)
            logger.debug(csv_file.content_type_extra)

            # TODO: Add support for TSV (why not?)
            # pandas delimiter autodetect didn't work with RPI sample data
            df = pd.read_csv(
                io.StringIO(csv_file.read().decode('utf-8')),
                delimiter=',',
            )

            logger.debug(f'rows before: {len(df)}')
            self.message_user(request, f'rows before: {len(df)}',
                              level=messages.ERROR)

            # find rows of all null columns
            dfAllNull = df.isnull().all(axis='columns')

            # skip rows of all null, lower case columns,
            # rename "phrase" column for backwards compatibility
            df = df[~dfAllNull] \
                .rename(columns=lambda s: s.lower().strip()) \
                .rename(columns={'phrase': 'topic'})

            # lower case month names
            df['month'] = df['month'].apply(str.lower)
            logger.debug(df)
            logger.debug(f'rows after: {len(df)}')
            self.message_user(request, f'rows after: {len(df)}',
                              level=messages.SUCCESS)

            # dictionary of month name/abbr to number
            months = {month.lower(): index for index, month in
                      list(enumerate(calendar.month_name[1:], 1)) +
                      list(enumerate(calendar.month_abbr[1:], 1))}

            # TODO: remove `head(n)` after debugging is done
            for row in df.head(8).itertuples():
                logger.debug(row)
                self.message_user(request, row)

                # TODO: count number of topic/item created
                topic, created = Topic.objects.get_or_create(name=row.topic)
                self.message_user(request, topic)

                item, created = Item.objects.get_or_create(name=row.item,
                                                           topic=topic)
                self.message_user(request, item)

                itemPage, created = ItemPage.objects.get_or_create(
                    item=item, page=row.page,
                    month=months[row.month], year=row.year)
                self.message_user(request, itemPage)

            self.message_user(request, 'The CSV file has been imported.')
            return redirect('..')
        form = CsvImportForm()
        context = {'form': form}
        return render(
            request, 'admin/csv_form.html', context
        )


@register(models.Topic)
class TopicAdmin(ModelAdmin):
    class TopicNoteInline(KarpeLiberTabularInline):
        model = models.TopicNote
        fk_name = model.topic.field.name

    class ItemInline(KarpeLiberTabularInline):
        model = models.Item


    inlines = [
        TopicNoteInline,
        ItemInline,
    ]


@register(models.Item)
class ItemAdmin(ModelAdmin):
    class ItemNoteInline(KarpeLiberTabularInline):
        model = models.ItemNote
        fk_name = model.item.field.name

    class ItemPageInline(KarpeLiberTabularInline):
        model = models.ItemPage
        readonly_fields = ['dateCalc', ]

    inlines = [
        ItemNoteInline,
        ItemPageInline,
    ]


@register(models.Volume)
class VolumeAdmin(ModelAdmin):
    readonly_fields = [
        'libraryLink',
    ]

    def libraryLink(self, topic):
        return format_html('<a target="_blank" href="{url}">{url}</a> ↗️',
                           url=topic.url)

    libraryLink.short_description = 'Library link'


# register all unregistered models to appear in admin UI
# TODO: add a flag to models to indicate whether they should be shown/hidden
registeredModelClasses = [cls.__name__ for cls in site._registry.keys()]

site.register(
    [cls for cls in models.__dict__.values() if
     isinstance(cls, type) and cls.__name__ not in registeredModelClasses])
