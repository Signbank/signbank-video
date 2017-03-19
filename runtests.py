import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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
            "bootstrap3",
            "video",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),

        TEMPLATES = [
          {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
                  'DIRS': [os.path.join((os.path.dirname(os.path.abspath(__file__))),
                        'tests', 'templates'),
            # insert your TEMPLATE_DIRS here

          ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                                ],
                    },
                 },
        ],

        LANGUAGE_NAME = "Auslan",
        COUNTRY_NAME = "Australia",
        SITE_TITLE = "Signbank",

        MEDIA_ROOT = os.path.join((os.path.dirname(os.path.abspath(__file__))),
          "tests", "testmedia"),
        VIDEO_UPLOAD_LOCATION = "upload",
        GLOSS_VIDEO_DIRECTORY = "video",

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
