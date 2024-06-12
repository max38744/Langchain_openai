from django.contrib import admin
from .models import *
from import_export.admin import ImportExportMixin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

models = apps.get_models()

for model in [QueryLog, Topic]:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass


class ChromaDBAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['category', 'QA']

admin.site.register(ChromaDB, ChromaDBAdmin)