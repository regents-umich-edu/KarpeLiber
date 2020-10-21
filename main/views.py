import csv
import datetime
import io

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render


def index(_):
    return HttpResponse("Hello, world. You're at the main index.")


@permission_required('admin.can_add_log_entry')
def topic_upload(request):
    # TODO: why importing above causes "Apps aren't loaded yet" error?
    from main.models import Topic
    template = 'topic_upload.html'

    context = {
        'order': 'Order of the CSV columns should be...',
    }

    if request.method == 'GET':
        return render(request, template, context)

    csv_file = request.FILES['file']

    # FIXME: this is inconclusive
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Not a CSV file!')

    data_set = csv_file.read().decode('UTF-8')

    # TODO: replace below with pandas CSV support
    io_string = io.StringIO(data_set)
    next(io_string)  # skip CSV header line

    status = []

    for row in csv.reader(io_string, delimiter=',', quotechar='"'):
        _, created = Topic.objects.update_or_create(
            name=row[0],
            dateAdded=datetime.datetime.now(),
            dateUpdated=datetime.datetime.now(),
        )
        status.append(f'{row[0]}: {"Created" if created else "Skipped"}')

    context = {
        'results': status,
    }

    return render(request, template, context)
