# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 10:36
from video.models import TaggedVideo, Video
from django.db import models
from django.core.management.base import LabelCommand

# define this model here so that we can migrate from it to TaggedVideo
class GlossVideo(models.Model):
    """Legacy video model"""

    videofile = models.FileField("video file")
    gloss = models.ForeignKey('dictionary.Gloss')
    version = models.IntegerField("Version", default=0)


class Command(LabelCommand):
    help = 'Convert from GlossVideo to TaggedVideo models of videos'

    def handle_label(self, label, **options):
        """Copy all glossvideos to taggedvideo instances"""

        self.stdout.write("handling " + label)

        if label == 'copy':
            self.stdout.write("Copying")
            for gv in GlossVideo.objects.all():
                tv, created = TaggedVideo.objects.get_or_create(category='Gloss', tag=str(gv.gloss.pk))
                vid = Video(tag=tv, videofile=gv.videofile, version=gv.version)
                vid.save()

        elif label == 'revert':
            done = TaggedVideo.objects.all().delete()
            self.stdout.write(str(done))
