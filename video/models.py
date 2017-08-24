import os

from django.db import models, transaction, IntegrityError
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ObjectDoesNotExist

from video.convertvideo import extract_frame, convert_video


class TaggedVideoManager(models.Manager):
    """Manager for TaggedVideo that deals with versions
    of videos"""

    def add(self, content_type, object_id, videofile):
        """Add a new video associated with this object_id and content_type,
        increment version numbers for any older videos"""

        # do we have an existing TaggedVideo object for this content_type and object_id?
        tv, created = self.get_or_create(content_type__id=content_type, object_id=object_id)
        if not created:
            # increment version numbers of all other videos for this object_id
            for v in tv.video_set.all():
                v.version += 1
                v.save()

        video = Video(videofile=videofile, tag=tv, version=0)
        video.save()

        return tv

    def get_for_object(self, obj):
        """
        Create a queryset matching all TaggedVideos associated with the given object.
        """
        content_type = ContentType.objects.get_for_model(obj)
        try:
            return self.get(content_type__pk=content_type.pk, object_id=obj.pk)
        except ObjectDoesNotExist:
            return None


class TaggedVideo(models.Model):
    """A video that can be tagged with a content_type (eg. gloss, definintion, feedback)
    and a object_id (eg. the gloss id) """

    objects = TaggedVideoManager()

    content_type = models.ForeignKey(ContentType, verbose_name="content type", on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField("object id", db_index=True)
    object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = (("content_type", "object_id"),)

    @property
    def video(self):
        """Return only the most recent video version for this TaggedVideo."""
        return Video.objects.filter(tag=self).order_by('version').first()
        #return Video.objects.get(tag=self, version=0)

    def videos(self):
        """Return all videos for this TaggedVideo."""
        return Video.objects.filter(tag=self).order_by('version')

    def get_absolute_url(self):
        return self.video.get_absolute_url()

    def poster_url(self):
        return self.video.poster_url()

    def versions(self):
        """Return a count of the number of versions
        of videos for this tag"""
        return self.video_set.all().count()

    def revert(self):
        """Revert to the previous version of the video for this TaggedVideo,
        deletes the video with lowest version.
        Return True if an old version was removed,
        False if there was only one version or
        if something went wrong"""

        # need to have more than one version
        if self.versions() > 1:
            current = self.video
            try:
                with transaction.atomic():
                    current.delete()
                    # Make sure there aren't gaps between versions
                    for i, video in enumerate(self.video_set.all().order_by('version')):
                        video.version = i
                        video.save()
                    return True
            except IntegrityError:
                return False
        else:
            return False

    def __str__(self):
        return "%s/%s" % (self.content_type, self.object_id)


class TaggedVideoStorage(FileSystemStorage):
    """Implement our shadowing video storage system"""

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(TaggedVideoStorage, self).__init__(location, base_url)

    def get_valid_name(self, name):
        """Generate a valid name, we use directories named for the
        first two digits in the filename to partition the videos"""
        (targetdir, basename) = os.path.split(name)
        path = os.path.join(str(basename)[:2], str(basename))
        result = os.path.join(targetdir, path)
        return result


class Video(models.Model):
    """An uploaded video"""
    videofile = models.FileField("video file",
                                 upload_to=settings.GLOSS_VIDEO_DIRECTORY,
                                 storage=TaggedVideoStorage())
    tag = models.ForeignKey(TaggedVideo)

    # video version, most recent is 0
    version = models.IntegerField("Version", default=0)

    def get_absolute_url(self):
        return self.videofile.url

    def __poster_path(self, create=True):
        '''
        Return the path of the poster image for this
        video, if create=True, create the image if needed
        Return None if create=False and the file doesn't exist
        '''
        vidpath, ext = os.path.splitext(self.videofile.path)
        poster_path = vidpath + ".jpg"
        if not os.path.exists(poster_path):
            if create:
                extract_frame(self.videofile.path, poster_path)
            else:
                return None
        return poster_path

    def poster_url(self):
        """Return the URL of the poster image for this video"""
        # generate the poster image if needed
        path = self.__poster_path()
        # splitext works on urls too!
        vidurl, ext = os.path.splitext(self.videofile.url)
        poster_url = vidurl + ".jpg"
        return poster_url

    def delete_files(self):
        """Delete the files associated with this object"""
        try:
            os.unlink(self.videofile.path)
            poster_path = self.__poster_path(create=False)
            if poster_path:
                os.unlink(poster_path)
        except:
            pass
