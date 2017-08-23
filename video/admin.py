from django.contrib import admin

from video.models import TaggedVideo, Video


class VideoAdmin(admin.TabularInline):
    model = Video


@admin.register(TaggedVideo)
class TaggedVideoAdmin(admin.ModelAdmin):
    list_display = ('object', 'content_type', 'object_id',)
    search_fields = ['^object_id', 'content_type__model', 'video__videofile']
    list_filter = ('content_type',)
    inlines = [VideoAdmin]
