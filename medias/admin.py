from django.contrib import admin
from .models import Photo, Video


class PhotoAdmin(admin.ModelAdmin):
    pass


class VideoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Video, VideoAdmin)
