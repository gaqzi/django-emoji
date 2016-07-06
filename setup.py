# encoding: utf-8
import os
from setuptools import setup, find_packages

readme_file = os.path.join(os.path.dirname(__file__), 'README.rst')
README = None
try:
    f = open(readme_file, encoding='utf-8')
except TypeError:
    f = open(readme_file)
else:
    README = f.read()
    f.close()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-emoji',
    version='2.2.0',
    packages=find_packages(exclude=('test',)),
    include_package_data=True,
    license='BSD License',
    description='A simple django app to use emojis on your website',
    long_description=README,
    url='https://github.com/gaqzi/django-emoji/',
    author='Björn Andersson',
    author_email='ba@sanitarium.se',
    install_requires=[
        'django',
    ],
    tests_require=[
        'django_nose',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
