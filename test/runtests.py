import os
import sys
from django.conf import settings

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='testurlconf',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django.contrib.staticfiles',
        'emoji',
    ),
    STATIC_URL='/static/',
    TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), 'templates'),)
)

from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(['emoji', ])
if failures:
    sys.exit(failures)
