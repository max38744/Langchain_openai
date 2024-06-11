from django.contrib import admin
from .models import *
from import_export.admin import ImportExportMixin

admin.site.register(QueryLog)

class ChromaDBAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['category', 'QA']

admin.site.register(ChromaDB, ChromaDBAdmin)