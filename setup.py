# encoding: utf-8
import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-emoji',
    version='1.0',
    packages=['emoji'],
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
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
