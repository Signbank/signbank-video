from django.contrib import admin

from video.models import Video, GlossVideo 


class GlossVideoAdmin(admin.ModelAdmin):
    search_fields = ['^gloss']
    
    
admin.site.register(GlossVideo, GlossVideoAdmin)
