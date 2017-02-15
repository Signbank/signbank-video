=============================
signbank-video
=============================

.. image:: https://badge.fury.io/py/signbank-video.png
    :target: https://badge.fury.io/py/signbank-video

.. image:: https://travis-ci.org/hujosh/signbank-video.png?branch=master
    :target: https://travis-ci.org/hujosh/signbank-video

.. image:: https://codecov.io/gh/hujosh/signbank-video/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/hujosh/signbank-video

A Django application to handle video storage, designed to support the Signbank sign language
dictionary application.  This basically provides a video store where videos can be
associated with a category and a tag - both string values.   The category is
intended to be something like the name of the model that you want to associate
the video with (eg. Gloss), the tag is a unique identifier (eg. the sign IDgloss).
Videos can be referenced by the combination of category and tag labels.

Quickstart
----------

Install signbank-video::

    pip install signbank-video

Then use it in a project::

    import video

You must define the following variables in ``settings.py``:

* ``FFMPEG_PROGRAM = "/usr/bin/ffmpeg``
* ``FFMPEG_TIMEOUT = 60``
* ``FFMPEG_OPTIONS = ["-vcodec", "h264", "-an"]``
* ``VIDEO_ASPECT_RATIO = 3.0/4.0``

These variables control ``ffmpeg``, a program that the video app requires
and uses for extracting a frame from a video (a frame is a thumbnail).
You can download it here: https://www.ffmpeg.org/download.html.
The value of ``FFMPEG_PROGRAM`` on my system is ``/usr/bin/ffmpeg``, but on
your system it might be different; it all depends on where the installer puts
the ``ffmpeg`` executable.

Your must also define these following variables in ``settings.py``:

* ``VIDEO_UPLOAD_LOCATION = "upload"``
* ``GLOSS_VIDEO_DIRECTORY = "video"``
* ``MEDIA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), media)``

``MEDIA_ROOT`` is the root directory for your media, so for the video app it's the
root directory for all of the videos. ``VIDEO_UPLOAD_LOCATION``, and
``GLOSS_VIDEO_DIRECTORY`` are directories inside of ``MEDIA_ROOT`` that contain
user uploaded videos, and videos of each sign, respectively.

You must also define these following variables in ``settings.py``:

* ``LANGUAGE_NAME = "Auslan"``
* ``COUNTRY_NAME = "Australia"``
* ``SITE_TITLE = "Signbank"``

Finally, you must also add ``video`` to the ``INSTALLED_APPS`` variable of
``settings.py``.

Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
