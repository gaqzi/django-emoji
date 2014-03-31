============
django-emoji
============

.. image:: https://travis-ci.org/gaqzi/django-emoji.png?branch=master
           :target: https://travis-ci.org/gaqzi/django-emoji

.. image:: https://pypip.in/version/django-emoji/badge.png
    :target: https://pypi.python.org/pypi/django-emoji/
    :alt: Latest Version

.. image:: https://pypip.in/download/django-emoji/badge.png
    :target: https://pypi.python.org/pypi/django-emoji/
    :alt: Downloads

Emoji is a port of the GitHub gem `gemoji`_ to Django.

This app got two main use cases:

1. It'll try to replace items between :: with emojis, for instance ``: dog :`` (without the spaces) will become an emoji of a dog (:dog:).
2. It'll try to replace unicode characters with emojis, for instance '✌️' with a victory symbol (:v:).

.. _gemoji: https://github.com/github/gemoji

Quick start
-----------

1. Install `django-emoji`_ from PyPi::

      pip install django-emoji

.. _django-emoji: https://pypi.python.org/pypi/django-emoji

2. Add "emoji" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'emoji',
      )

3. Include the emoji URLconf in your project urls.py like this if you want to be able to get a JSON list of emojis::

      url(r'^emoji/', include('emoji.urls')),

4. Visit http://127.0.0.1:8000/emoji/all.json to get a json object with all emojis avilable

Usage
=====

API
----

Python
------

The Python class ``Emoji`` is a singleton and will return the same
instance between instantiations. On load Emoji will load the name of
all the emjis and their unicode equivalents into memory.

============================================= ===============================
               Call                                  Description
============================================= ===============================
``Emoji.names()``                             A list of all known emojis
``Emoji.replace(replacement_string)``         Replaces all emojies between ``::``
``Emoji.name_for(character)``                 The name for a given unicode character
``Emoji.replace_unicode(replacement_string)`` Replaces all known unicode emojies
============================================= ===============================

Javascript
----------

The browser version caches all the emojies in ``localStorage`` so
there won't be that many roundtrips to the server just to get a list
of the emojies.

**NOTE**: Depends on jQuery or some other library that exports ``$.get``.

==================================== ========================================
               Call                                  Description
==================================== ========================================
``Emoji.setDataUrl(url)``            Where to fetch the list of all available emojis
``Emoji.load()``                     Load all emojis from the server
``Emoji.get(/*emoji*/)``             Get the URL to an emoji of a name or return the names of all known emojis
``Emoji.replace(replacementString)`` Replace all ``::`` style emojis with images
``Emoji.clear()``                    Empty the browser cache
==================================== ========================================

Examples
--------

Replace an emoji using Python templates by loading the tags in your template::

      {% load emoji_tags %}
      {{ blog_post.body|emoji_replace }}
      {{ blog_post.body|emoji_replace_unicode }}

Replace emojis using Javascript (to for instance show a preview before the user saves what it is they are writing)::

      {% load emoji_tags %}

      <script src="{% static 'emoji/js/emoji.js' %}"></script>
      {% emoji_load %}

      Emoji.get('dog') // => url stub to dog emoji or falsy
      Emoji.get() // => all emojis available

      Emoji.replace("It's raining :cats: and :dogs:.") // => It's raining <img src="..." alt="cats" class="emoji"> and <img src="..." alt="dogs" class="emoji">

What ``emoji_load`` does is that it sets the endpoint to retrieve the listing of all the available emojis and thus only works if the emoji urls has been included.

It is the equivalent of doing::

      Emoji.setDataUrl('{% url 'emoji:list.json' %}').load();

Which is also available as template stub::

      {% include 'emoji/script.html' %}

Usage from inside Python where the Emoji class mimics some of the behavior of a dict::

      from emoji import Emoji
      Emoji['dog'] # => url stub to dog emoji or None
      'dog' in Emoji # => True
      Emoji.keys() # => a list of all emojis by name
      Emoji.replace("It's raining :cats: and :dogs:") # => It's raining <img src="..." alt="cats" class="emoji"> and <img src="..." alt="dogs" class="emoji">


Replacing unicode Emojis
------------------------

Emoji has the ability to give you the name of an emoji from a unicode
character. It can also replace every instance of emoji characters in a
string with their image replacements.

Usage::

      >>> from emoji import Emoji
      >>> Emoji.name_for(u'\U000148b')
      kiss
      >>> Emoji.replace_unicode(u'I send a \U0001f48b!')
      I send a <img src="/static/emoji/img/kiss.png" alt="kiss" class="emoji">

**Note**:

To be able to use the unicode replacements your Python version needs
to be built with wide unicode character support. This seems to be the
case for most Pythons available from package managers. If you do not
have wide character support then an exception will be raised::

      >>> print(unichr(0x0001f48b))
      ValueError: unichr() arg not in range(0x10000) (narrow Python build)
