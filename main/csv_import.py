import calendar
import io
import logging
from datetime import datetime

import pandas as pd
from django import forms
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.core.exceptions import MultipleObjectsReturned
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import redirect, render
from django.urls import path

from main.models import Volume, Topic, Item, ItemPage

logger = logging.getLogger(__name__)


class CsvImportForm(forms.Form):
    """
    Form used by ModelAdminCsvImport
    """
    csv_file = forms.FileField()
    csv_file.widget.attrs.update({'accept': '.csv'})
    csv_file.label = 'CSV file'
    csv_file.help_text = (
        '<br/>Choose a CSV file with columns named <tt>topic</tt>, '
        '<tt>item</tt>, <tt>page</tt>, <tt>year</tt>, and <tt>month</tt>.')
    csv_file.required = True

    volume = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={
            'onchange': 'if (this.value == "new") '
                        '{window.location.href = "/admin/main/volume/add/"}'}))
    volume.label = 'Volume'
    volume.help_text = (
        '<br/>Select a volume to import into or '
        '<a href="/admin/main/volume/add/">create a new volume</a>.')
    volume.required = True

    def __init__(self, *args, **kwargs):
        if 'volume' in kwargs:
            volume = kwargs.pop('volume')
        super().__init__(*args, **kwargs)
        self.fields['volume'].queryset = Volume.objects.all().order_by(
            '-dateEnd')
        choices = list(self.fields['volume'].choices)
        choices.insert(1, ('new', '✨ Create a new volume'))
        self.fields['volume'].choices = choices
        if volume and volume.isnumeric():
            self.fields['volume'].initial = int(volume)


class ModelAdminCsvImport(ModelAdmin):
    """
    Add CSV import feature to top of admin change lists

    Possible features:
    1. Support Excel files directly without conversion to CSV.
    2. Read data from Google Sheets or Google Drive.
    """
    change_list_template = 'admin/csv_import_change_list.html'

    def get_urls(self):
        return [path('import-csv/', self.import_csv), ] + super().get_urls()

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file: InMemoryUploadedFile = request.FILES['csv_file']
            volume = Volume.objects.get(pk=request.POST['volume'])
            logger.debug(csv_file)

            # TODO: use content_type for validation
            logger.debug(csv_file.content_type)

            # TODO: Add support for TSV (why not?)
            # pandas delimiter autodetect didn't work with RPI sample data
            df = pd.read_csv(
                io.StringIO(csv_file.read().decode('utf-8')),
                delimiter=',',
            )

            logger.debug(f'rows before: {len(df)}')
            self.message_user(request, f'rows before: {len(df)}',
                              level=messages.ERROR)

            # TODO: Strip whitespace from ends of all column values
            # AI: df = df.applymap(
            #     lambda x: x.strip()
            #     if isinstance(x, str) else x)

            # TODO: report column values with leading or trailing whitespace
            # AI: df.applymap(
            #     lambda x: x
            #     if isinstance(x, str) and x.strip() == x else None)

            # find rows of all null columns
            dfAllNull = df.isnull().all(axis='columns')

            # skip rows of all null, lower case columns,
            # rename "phrase" for backwards compatibility,
            # make "year" integer for datetime compatibility
            df = df[~dfAllNull] \
                .rename(columns=lambda s: s.lower().strip()) \
                .rename(columns={'phrase': 'topic'}) \
                .astype({'year': int})

            # TODO: Add check for all required columns
            # topic, item, page, year, month

            # dictionary of month name/abbr to number
            months = {month.lower(): index for index, month in
                      list(enumerate(calendar.month_name[1:], 1)) +
                      list(enumerate(calendar.month_abbr[1:], 1))}

            # lower case month names, convert to number
            df['month'] = df['month'].apply(str.lower).apply(months.get)
            logger.debug(df)
            logger.debug(f'rows after: {len(df)}')
            self.message_user(request, f'rows after: {len(df)}',
                              level=messages.SUCCESS)

            newTopics, newItems = 0, 0
            for row in df.itertuples():
                logger.debug(row)
                self.message_user(request, row)

                # TODO: count number of topic/item created
                topic, new = Topic.objects.get_or_create(name=row.topic)
                self.message_user(request, topic)
                if new:
                    newTopics += 1

                try:
                    item, new = Item.objects.get_or_create(name=row.item,
                                                           topic=topic)
                except MultipleObjectsReturned:
                    item = Item.objects.filter(name=row.item,
                                               topic=topic).first()
                    new = False

                self.message_user(request, item)
                if new:
                    newItems += 1

                itemPage, _ = ItemPage.objects.get_or_create(
                    item=item, page=row.page,
                    date=datetime(row.year, row.month, 1),
                    volume=volume, )
                self.message_user(request, itemPage)

            self.message_user(request, f'{newTopics} new topics, '
                                       f'{newItems} new items')
            self.message_user(request, f'The file "{csv_file.name}" '
                                       f'has been imported.')
            return redirect('..')
        form = CsvImportForm(volume=request.GET.get('volume'))
        context = {'form': form}
        return render(
            request, 'admin/csv_form.html', context
        )
