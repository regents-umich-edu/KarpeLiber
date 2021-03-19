from django.contrib.admin import site, register, ModelAdmin, \
    TabularInline
from django.contrib.auth.decorators import permission_required
from django.utils.html import format_html

from main import models
# TODO: learn about django_extensions.logging
# from django_extensions import logging
# from main.reverseadmin import ReverseModelAdmin
from main.csv_import import ModelAdminCsvImport
from .models import Topic


class KarpeLiberTabularInline(TabularInline):
    extra = 0  # don't show "add another" rows by default
    show_change_link = True


@register(Topic)
class TopicAdmin(ModelAdmin):
    class TopicNoteInline(KarpeLiberTabularInline):
        model = models.TopicNote
        fk_name = model.topic.field.name

    class ItemInline(KarpeLiberTabularInline):
        model = models.Item

    inlines = (
        TopicNoteInline,
        ItemInline,
    )
    search_fields=(Topic.name.field.name,)


@register(models.Item)
class ItemAdmin(ModelAdminCsvImport):
    class ItemNoteInline(KarpeLiberTabularInline):
        model = models.ItemNote
        fk_name = model.item.field.name

    class ItemPageInline(KarpeLiberTabularInline):
        model = models.ItemPage

    inlines = (
        ItemNoteInline,
        ItemPageInline,
    )
    search_fields=(models.Item.name.field.name,)


@register(models.ItemPage)
class ItemPageAdmin(ModelAdminCsvImport):
    pass


@register(models.Volume)
class VolumeAdmin(ModelAdmin):
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

    def listDisplayLibraryLink(self, volume):
        return format_html('<a target="_blank" href="{url}">↗️</a>',
                           url=volume.url)

    listDisplayLibraryLink.short_description = ''

    def libraryLink(self, volume):
        return format_html('<a target="_blank" href="{url}">{url}</a> ↗️',
                           url=volume.url)

    libraryLink.short_description = 'Library link'


# register all unregistered models to appear in admin UI
# TODO: add a flag to models to indicate whether they should be shown/hidden
site.register(
    [model for model in models.__dict__.values() if
     isinstance(model, type) and not site.is_registered(model)])
