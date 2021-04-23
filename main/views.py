import logging
from typing import Tuple, Optional

from django.db.models import QuerySet, Count
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render

from main.models import Topic, ItemPage
from main.util import safeInt

logger = logging.getLogger(__name__)


def index(_):
    return HttpResponse('This is the main index.')


def search(request: HttpRequest):
    # whitespace: strip leading/trailing & reduce embedded
    searchString: str = ' '.join(request.GET.get('searchString', '').split())

    topicId: Optional[int] = safeInt(
        request.GET.get('phraseId', request.GET.get('topicId')))
    moreTopics: Optional[int] = safeInt(
        request.GET.get('morePhrases', request.GET.get('moreTopics')))
    moreItems: Optional[int] = safeInt(request.GET.get('moreItems'))

    topic: QuerySet = None
    topics: QuerySet = None
    itemPages: QuerySet = None

    maxTopics = 25 if moreTopics is not None else 15
    maxItems = 25 if moreItems is not None else 10

    itemPagesOrderFields: Tuple[str, ...] = ('-year', 'page', 'item__name')
    itemPagesFilterArgs: Optional[dict[str, str]] = None

    if searchString or topicId:
        if topicId:
            topic = get_object_or_404(Topic, pk=topicId)
            logger.debug(topic)

            itemPagesFilterArgs = {'item__topic': topic}
        elif not moreItems:
            topics = (Topic.objects.filter(name__icontains=searchString)
                      .annotate(itemCount=Count('items__itemPages'))
                      .order_by('name'))
            logger.debug(topics)

        if itemPagesFilterArgs is None:
            itemPagesFilterArgs = {'item__name__icontains': searchString}

        if not moreTopics:
            itemPages = (ItemPage.objects.filter(**itemPagesFilterArgs)
                         .order_by(*itemPagesOrderFields))
            logger.debug(itemPages)

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
            if moreItems == len(itemPages):
                moreItems -= maxItems
            if moreItems < 0:
                moreItems = 0
            elif moreItems > len(itemPages):
                moreItems = len(itemPages) - (len(itemPages) % maxItems)
            if moreItems == len(itemPages):
                moreItems -= maxItems

        topicIndex: int = 0 if not moreTopics else moreTopics
        itemIndex: int = 0 if not moreItems else moreItems

        return render(request, 'main/search.html', {
            'searchString': searchString,
            'topic': topic,
            'topics':
                topics[topicIndex:topicIndex + maxTopics] if topics else None,
            'topicsTotalCount': topics.count() if topics else None,
            'itemPages': itemPages[itemIndex:itemIndex + maxItems] if itemPages else None,
            'itemPagesTotalCount': itemPages.count() if itemPages else None,
            'moreTopics': moreTopics,
            'moreItems': moreItems,
            'maxTopics': maxTopics,
            'maxItems': maxItems,
        })
    else:
        return render(request, 'main/search.html')
