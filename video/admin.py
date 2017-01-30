from django.contrib import admin

from video.models import TaggedVideo, Video

class VideoAdmin(admin.TabularInline):
    model = Video

@admin.register(TaggedVideo)
class TaggedVideoAdmin(admin.ModelAdmin):
    search_fields = ['^tag']
    inlines = [VideoAdmin]
