from django.contrib import admin

# Register your models here.
from ArtHub.art.models import ArtPiece, News, Event


@admin.register(ArtPiece)
class ArtAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title',)
