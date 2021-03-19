import logging
# from datetime import datetime, timezone

from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.utils import timezone

from main.models import Topic, Item

logger = logging.getLogger(__name__)

def index(_):
    return HttpResponse('This is the main index.')


def safeInt(x, base=10):
    try:
        result = int(x, base)
    except (ValueError, TypeError):
        result = None
    return result


def search(request: HttpRequest):
    # x = datetime.now(timezone.utc)
    y = timezone.localize()
    searchString: str = request.GET.get('searchString')
    moreTopics: int = safeInt(
        request.GET.get('morePhrases', request.GET.get('moreTopics')))
    moreItems: int = safeInt(request.GET.get('moreItems'))

    logger.debug(searchString)

    topics: QuerySet = None
    items: QuerySet = None
    if searchString:
        # topics = Topic.objects.filter(name__icontains=searchString)
        topics = Topic.objects.filter(name__icontains='baird')
        logger.debug(topics)
        # items = Item.objects.filter(name__icontains=searchString)
        items = Item.objects.filter(name__icontains='award')
        logger.debug(items)
        for item in items:
            logger.debug(item.itemPages.all())

    return render(request, 'main/search.html', {
        'searchString': searchString,
        'topics': topics,
        'items': items,
        'moreTopics': moreTopics,
        'moreItems': moreItems,
    })

    # return HttpResponse(
    #     f'This is the search feature. Search text: '
    #     f'{"n/a" if searchString is None else repr(searchString)}')
