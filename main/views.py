import logging
from typing import Tuple, Optional

from django.db.models import Count, IntegerField, Q, QuerySet
from django.db.models.functions import Cast, Coalesce
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render

from main.models import Topic, ItemPage
from main.util import safeInt, queryAllWords

logger = logging.getLogger(__name__)


def index(_):
    return HttpResponse('This is the main index.')


def search(request: HttpRequest):
    templateName: str = 'main/search.html'

    # whitespace: strip leading/trailing & reduce embedded
    searchString: str = ' '.join(request.GET.get('searchString', '').split())

    searchError: str = None
    if searchString and len(searchString) < 2:
        searchError = 'Please enter two or more characters ' \
                      'to perform a search.'

    topicId: Optional[int] = safeInt(
        request.GET.get('phraseId', request.GET.get('topicId')))
    moreTopics: Optional[int] = safeInt(
        request.GET.get('morePhrases', request.GET.get('moreTopics')))
    moreItems: Optional[int] = safeInt(request.GET.get('moreItems'))

    topic: QuerySet = None
    topics: QuerySet = None
    items: QuerySet = None
    maxTopics: int = None
    maxItems: int = None

    if not searchError:

        if moreTopics is not None:
            maxTopics = 25
            templateName = 'main/topics.html'
        else:
            maxTopics = 15

        if moreItems is not None:
            maxItems = 25
            templateName = 'main/items.html'
        else:
            maxItems = 10

        # sort_date:  item date if present, otherwise volume dateBegin
        itemOrderFields: Tuple[str, ...] = ('-sort_date', '-page',
                                            'item__name')

        itemFilterArgs: Optional[Q] = None

        if searchString or topicId:
            if topicId:
                topic = get_object_or_404(Topic, pk=topicId)
                logger.debug(topic)

                itemFilterArgs = Q(('item__topic', topic))
                templateName = 'main/topicItems.html'

                if moreItems is None:
                    moreItems = 0

            elif not moreItems:
                topics = (Topic.objects
                          .filter(
                    queryAllWords('name__icontains', searchString))
                          .annotate(itemCount=Count('items__itemPages'))
                          .order_by('name'))
                logger.debug(topics)

            if itemFilterArgs is None:
                itemFilterArgs = queryAllWords('item__name__icontains',
                                               searchString)

            if not moreTopics:
                items = (
                    ItemPage.objects
                    .annotate(sort_date=Coalesce('date', 'volume__dateBegin'))
                    .filter(itemFilterArgs)
                    .order_by(*itemOrderFields)
                )

    if moreTopics:
        if moreTopics == len(topics):
            moreTopics -= maxTopics
        if moreTopics < 0:
            moreTopics = 0
        elif moreTopics > len(topics):
            moreTopics = len(topics) - (len(topics) % maxTopics)
        if moreTopics == len(topics):
            moreTopics -= maxTopics

    if moreItems:
        if moreItems == len(items):
            moreItems -= maxItems
        if moreItems < 0:
            moreItems = 0
        elif moreItems > len(items):
            moreItems = len(items) - (len(items) % maxItems)
        if moreItems == len(items):
            moreItems -= maxItems

    topicIndex: int = 0 if not moreTopics else moreTopics
    itemIndex: int = 0 if not moreItems else moreItems

    return render(request, templateName, {
        'searchString': searchString,
        'searchError': searchError,
        'topic': topic,
        'topicId': topicId,
        'topics': (topics[topicIndex:topicIndex + maxTopics]
                   if topics else None),
        'topicsTotalCount': topics.count() if topics else None,
        'items': (items[itemIndex:itemIndex + maxItems]
                  if items else None),
        'itemsTotalCount': items.count() if items else None,
        'moreTopics': moreTopics,
        'moreItems': moreItems,
        'maxTopics': maxTopics,
        'maxItems': maxItems,
    })
