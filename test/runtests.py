import os
import sys

import django
from django.conf import settings

# Ensure that the folder that contains the emoji module is in path
package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, package_path)

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
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ),
    STATIC_URL='/static/',
    TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), 'templates'),),
)

if django.VERSION[0] == 1 and django.VERSION[1] >= 7:
    django.setup()

from django_nose import NoseTestSuiteRunner  # Can't be imported earlier
test_runner = NoseTestSuiteRunner()
failures = test_runner.run_tests(['emoji', ])
if failures:
    sys.exit(failures)
