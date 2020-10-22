import csv
import io
import logging

from django.contrib.admin import site, register, ModelAdmin, \
    TabularInline
from django.forms import forms
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.html import format_html

from main import models


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
            csv_file = request.FILES['csv_file']
            csv_raw_data = csv_file.read().decode('UTF-8')

            csv_strings = io.StringIO(csv_raw_data)
            # next(csv_strings)  # skip CSV header line

            reader = csv.reader(csv_strings)
            for line in reader:
                logger.debug(line)
            # Create objects from CSV data
            # ...
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
