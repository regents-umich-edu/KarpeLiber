import argparse
import logging

from django.core.management.base import BaseCommand

from main.indexformatter import IndexFormatter

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    VOLUME_ID = 'volumeId'
    TOPIC_DELIMITER = 'topicDelimiter'
    ITEM_DELIMITER = 'itemDelimiter'
    PAGE_DELIMITER = 'pageDelimiter'

    help = ('Produce a printable index for entries '
            'associated with a specific volume.')

    def add_arguments(self, parser):
        # usually uses Django's default formatter, DjangoHelpFormatter, which
        # puts our arguments first.  ArgumentDefaultsHelpFormatter shows
        # defaults, which Django doesn't do by default.  May need to make my
        # own formatter based on Django's, with the addition of showing
        # defaults.
        parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
        parser.add_argument(
            self.VOLUME_ID, type=int,
            help='ID number of the volume for which the index is to '
                 'be printed.  The ID number can be found in the admin '
                 'pages and is often the same as the year of the '
                 "volume's starting date.")
        parser.add_argument(
            f'--{self.TOPIC_DELIMITER}', type=str,
            default=IndexFormatter.TOPIC_DELIMITER_DEFAULT,
            help='Delimiter between topic and item.')
        parser.add_argument(
            f'--{self.ITEM_DELIMITER}', type=str,
            default=IndexFormatter.ITEM_DELIMITER_DEFAULT,
            help='Delimiter between items.')
        parser.add_argument(
            f'--{self.PAGE_DELIMITER}', type=str,
            default=IndexFormatter.PAGE_DELIMITER_DEFAULT,
            help='Delimiter between item and page number.')

    def handle(self, *args, **options):
        print(IndexFormatter(
            options[self.VOLUME_ID],
            topicDelimiter=options[self.TOPIC_DELIMITER],
            itemDelimiter=options[self.ITEM_DELIMITER],
            pageDelimiter=options[self.PAGE_DELIMITER]).format())
