from django.contrib.admin import site, register, ModelAdmin, \
    TabularInline
from django.utils.html import format_html

from main import models
# TODO: learn about django_extensions.logging
# from django_extensions import logging
# from main.reverseadmin import ReverseModelAdmin
from main.csv_import import ModelAdminCsvImport
from main.indexformatter import ModelAdminIndexFormatter
from .models import Topic, ItemNote, NoteType


class KarpeLiberTabularInline(TabularInline):
    extra = 0  # don't show "add another" rows by default
    show_change_link = True


@register(models.TopicNote)
class TopicNoteAdmin(ModelAdmin):
    raw_id_fields = (
        'topic',
        'referencedTopic',
    )


@register(Topic)
class TopicAdmin(ModelAdmin):
    class TopicNoteInline(KarpeLiberTabularInline):
        model = models.TopicNote
        fk_name = model.topic.field.name
        raw_id_fields = TopicNoteAdmin.raw_id_fields

    class ItemInline(KarpeLiberTabularInline):
        model = models.Item

    list_display = (
        'name',
        'numItems',
    )

    inlines = (
        TopicNoteInline,
        ItemInline,
    )
    search_fields = (Topic.name.field.name,)


@register(models.Item)
class ItemAdmin(ModelAdminCsvImport):
    list_display = (
        'name',
        'topic',
    )

    # TODO: raw_id fields are good, but bring up their own edit window
    # raw_id_fields = ()

    # TODO: autocomplete fields look better, but still bring up all FKs
    autocomplete_fields = (
        'topic',
    )

    class ItemNoteInline(KarpeLiberTabularInline):
        model = models.ItemNote
        fk_name = model.item.field.name

    class ItemPageInline(KarpeLiberTabularInline):
        model = models.ItemPage

    inlines = (
        ItemNoteInline,
        ItemPageInline,
    )
    search_fields = (models.Item.name.field.name,)


@register(models.ItemPage)
class ItemPageAdmin(ModelAdminCsvImport):
    raw_id_fields = (
        'item',
        'volume',
    )


@register(models.Volume)
class VolumeAdmin(ModelAdminIndexFormatter):
    list_display = (
        'title',
        'listDisplayLibraryLink',
        'dateBegin',
        'dateEnd',
        'pages',
        'available',
    )

    readonly_fields = (
        'libraryLink',
    )

    def listDisplayLibraryLink(self, volume) -> str:
        return format_html('<a target="_blank" href="{url}">↗️</a>',
                           url=volume.url) if volume.url else '⛔'

    listDisplayLibraryLink.short_description = ''

    def libraryLink(self, volume) -> str:
        return format_html('<a target="_blank" href="{url}">{url}</a> ↗️',
                           url=volume.url) if volume.url else 'n/a'

    libraryLink.short_description = 'Library link'


# register all unregistered models to appear in admin UI
# TODO: add a flag to models to indicate whether they should be shown/hidden
# site.register(
#     [model for model in models.__dict__.values() if
#      isinstance(model, type) and not site.is_registered(model)])
site.register([models.ItemNote, models.NoteType, models.PageMapping])
