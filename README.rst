============
django-emoji
============

Emoji is a port of the GitHub gem `gemoji`_ to Django.

It'll try to replace items between :: with emojis, for instance ``: dog :`` (without the spaces) will become an emoji of a dog (:dog:).

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
-----

Replace an emoji using Python templates by loading the tags in your template::

      {% load emoji_tags %}
      blog_post.body|emoji_replace

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
