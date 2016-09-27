import sys
import os

try:
    from django.conf import settings
    from django.test.utils import get_runner

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="tests.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "video",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
        

        LANGUAGE_NAME = "Auslan",
        COUNTRY_NAME = "Australia",
        SITE_TITLE = "Signbank",

        MEDIA_ROOT = os.path.join((os.path.dirname(os.path.abspath(__file__))),
          "tests", "testmedia"),
        VIDEO_UPLOAD_LOCATION = "upload",
        GLOSS_VIDEO_DIRECTORY = "video",
        
        FFMPEG_PROGRAM = "/usr/bin/ffmpeg",
        FFMPEG_TIMEOUT = 60,
        FFMPEG_OPTIONS = ["-vcodec", "h264", "-an"],
        


        # defines the aspect ratio for videos
        VIDEO_ASPECT_RATIO = 3.0/4.0
        
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    msg = "To fix this error, run: pip install -r requirements_test.txt"
    raise ImportError(msg)


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
