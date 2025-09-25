import logging
from itertools import groupby
from urllib.parse import quote

from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import path

from main.models import Volume, ItemPage

logger = logging.getLogger(__name__)


class IndexFormatter:
    """
    Format an index for printing.
    """
    TOPIC_DELIMITER_DEFAULT = ':'
    ITEM_DELIMITER_DEFAULT = ';'
    PAGE_DELIMITER_DEFAULT = ','

    def __init__(self, volumeId: int,
                 topicDelimiter: str = TOPIC_DELIMITER_DEFAULT,
                 itemDelimiter: str = ITEM_DELIMITER_DEFAULT,
                 pageDelimiter: str = PAGE_DELIMITER_DEFAULT):
        self.indexedVolume = get_object_or_404(Volume, id=volumeId)
        self.topicDelimiter: str = topicDelimiter
        self.itemDelimiter: str = itemDelimiter
        self.pageDelimiter: str = pageDelimiter

        # until `ItemPage.page` string is changed to an integer, it must
        # be converted for ordering; `int()` doesn't work here, so using `* 1`
        self.itemPages: QuerySet = (
            ItemPage.objects.filter(volume__id=volumeId)
            .order_by('item__topic__name', F('page') * 1, 'item__name'))

    def format(self) -> tuple[str, str]:
        """
        Format the index for printing.
        """
        previousLetter: str = ''
        indexText: str = ''

        topic: str
        topicLetter: str
        itemPages: QuerySet

        for (topic, topicLetter), itemPages in groupby(
                self.itemPages, lambda ip: (
                        (n := ip.item.topic.name), n[0].upper())):
            indexText += (
                    (f'\n{(previousLetter := topicLetter)}\n\n'
                     if previousLetter != topicLetter else '')
                    + f'{topic}{self.topicDelimiter} '
                    + f'{self.itemDelimiter} '.join(
                [f'{itemPage.item.name}{self.pageDelimiter} {itemPage.page}'
                 for itemPage in itemPages])
                    + '\n')

        return (indexText, self.indexedVolume.title)


class ModelAdminIndexFormatter(ModelAdmin):
    """
    Add CSV import feature to top of admin change lists

    Possible features:
    1. Support Excel files directly without conversion to CSV.
    2. Read data from Google Sheets or Google Drive.
    """
    # change_list_template = 'admin/csv_import_change_list.html'
    change_form_template = 'admin/index_formatter_change_form.html'

    @staticmethod
    def download_index_print(request, volumeId):
        (formattedIndex, volumeTitle) = IndexFormatter(volumeId).format()

        response = HttpResponse(formattedIndex, content_type='text/plain')
        filename = quote(f'index_{volumeTitle}_{volumeId}.txt')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    def get_urls(self):
        custom_urls = [
            path('<int:volumeId>/download-index-print/',
                 self.download_index_print, name='download-index-print'),
        ]
        return custom_urls + super().get_urls()

    def message(self, request=None, message=None, level=messages.INFO):
        """
        Send a message to the user
        """
        if request is None:
            print(message)
        else:
            self.message_user(request, message, level=level)
