import os

from django.db import models, transaction, IntegrityError
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .convertvideo import extract_frame, convert_video


class TaggedVideoManager(models.Manager):
    """Manager for TaggedVideo that deals with versions
    of videos"""

    def add(self, category, tag, videofile):
        """Add a new video associated with this tag and category
        increment version numbers for any older videos"""

        # add the category name into the videofile name
        videofile.name = "%s-%s" % (category, videofile.name)

        # do we have an existing TaggedVideo object for this category and tag?
        tv, created = self.get_or_create(category=category, tag=tag)
        if not created:
            # increment version numbers of all other videos for this tag
            for v in tv.video_set.all():
                v.version += 1
                v.save()

        video = Video(videofile=videofile, tag=tv, version=0)
        video.save()

        return tv


class TaggedVideo(models.Model):
    """A video that can be tagged with a category (eg. gloss, definition, feedback)
    and a tag (eg. the gloss id) """

    objects = TaggedVideoManager()

    category = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)

    class Meta:
        unique_together = (("category", "tag"),)

    @property
    def video(self):
        """Return the most recent video version for this tag"""

        return Video.objects.get(tag=self, version=0)

    def get_absolute_url(self):
        return self.video.get_absolute_url()

    def poster_url(self):
        return self.video.poster_url()

    def versions(self):
        """Return a count of the number of versions
        of videos for this tag"""

        return self.video_set.all().count()

    def revert(self):
        """Revert to the previous version of the video
        for this tag, deletes the current video.
        Return True if an old version was removed,
        False if there was only one version or
        if something went wrong"""

        # need to have more than one version
        if self.versions() > 1:
            current = self.video
            try:
                with transaction.atomic():
                    current.delete()
                    for video in self.video_set.all():
                        video.version -= 1
                        video.save()
                    return True
            except IntegrityError:
                return False
        else:
            return False

    def __str__(self):
        return "%s/%s" % (self.category, self.tag)


class TaggedVideoStorage(FileSystemStorage):
    """Implement our shadowing video storage system"""

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(TaggedVideoStorage, self).__init__(location, base_url)

    def get_valid_name(self, name):
        """Generate a valid name, we use directories named for the
        first two digits in the filename to partition the videos"""
        targetdir, basename = os.path.split(name)
        if '-' in basename:
            category, tag = basename.split('-', maxsplit=1)  # basename is eg. Gloss-1234.mp4
        else:
            category, tag = 'Base',  basename
        # we make a dirname from the first two letters of the tag
        # make it 00 if the basename is two digits or less
        if len(tag) <= 6:
            dirname = '00'
        else:
            dirname = str(tag)[:2]

        path = os.path.join(dirname, str(tag))
        result = os.path.join(targetdir, category, path)
        return result


class Video(models.Model):
    """An uploaded video"""
    videofile = models.FileField("video file",
                                 upload_to=settings.GLOSS_VIDEO_DIRECTORY,
                                 storage=TaggedVideoStorage())
    tag = models.ForeignKey(TaggedVideo, on_delete=models.CASCADE)

    # video version, most recent is 0
    version = models.IntegerField("Version", default=0)

    def get_absolute_url(self):
        return self.videofile.url

    def __poster_path(self, create=True):
        """
        Return the path of the poster image for this
        video, if create=True, create the image if needed
        Return None if create=False and the file doesn't exist
        """
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
