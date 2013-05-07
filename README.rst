=====
django-emoji
=====

This app is still under development and is on GitHub to ease with testing. Please ignore until version 1.0

Emoji is a port of the GitHub gem `gemoji`_ to Django.

Quick start
-----------

1. Add "emoji" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'emoji',
      )

2. Include the emoji URLconf in your project urls.py like this if you want to be able to get a JSON list of emojis::

      url(r'^emoji/', include('emoji.urls')),

3. Visit http://127.0.0.1:8000/emoji/ to get a json object with all emojis avilable

