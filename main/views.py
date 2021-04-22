import logging
from typing import Tuple

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

    topicId: int = safeInt(
        request.GET.get('phraseId', request.GET.get('topicId')))
    moreTopics: int = safeInt(
        request.GET.get('morePhrases', request.GET.get('moreTopics')))
    moreItems: int = safeInt(request.GET.get('moreItems'))

    topic: QuerySet = None
    topics: QuerySet = None
    itemPages: QuerySet = None

    itemPagesOrderFields: Tuple[str, ...] = ('-year', 'page', 'item__name')

    if searchString or topicId:
        if topicId:
            topic = get_object_or_404(Topic, pk=topicId)
            logger.debug(topic)

            itemPagesFilterArgs = {'item__topic': topic}
        else:
            topics = (Topic.objects.filter(name__icontains=searchString)
                      .annotate(itemCount=Count('items__itemPages'))
                      .order_by('name'))
            logger.debug(topics)

            itemPagesFilterArgs = {'item__name__icontains': searchString}

        itemPages = (ItemPage.objects.filter(**itemPagesFilterArgs)
                     .order_by(*itemPagesOrderFields))
        logger.debug(itemPages)

        return render(request, 'main/search.html', {
            'searchString': searchString,
            'topic': topic,
            'topics': topics[0:15] if topics else None,
            'topicsTotalCount': topics.count() if topics else None,
            'itemPages': itemPages[0:10] if itemPages else None,
            'itemPagesTotalCount': itemPages.count() if itemPages else None,
            'moreTopics': moreTopics,
            'moreItems': moreItems,
        })
    else:
        return render(request, 'main/search.html')
