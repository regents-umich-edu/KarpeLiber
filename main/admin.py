from django.contrib import admin

from main import models

# register all models to appear in admin UI
# TODO: add a flag to models to indicate whether they should be shown/hidden
for cls in models.__dict__.values():
    if isinstance(cls, type):
        admin.site.register(cls)
