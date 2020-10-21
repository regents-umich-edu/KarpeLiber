from django.contrib.admin import site, register, ModelAdmin, \
    TabularInline
from django.utils.html import format_html

from main import models

class KarpeLiberTabularInline(TabularInline):
    extra = 0 # don't show "add another" rows by default
    show_change_link = True

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
