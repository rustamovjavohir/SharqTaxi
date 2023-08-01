from django.contrib import admin
from apps.file.models import Image


@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    list_display = ('name', 'image', 'is_main')
    list_filter = ('name', 'image', 'is_main')

    class Meta:
        model = Image
        ordered = ('-id',)
