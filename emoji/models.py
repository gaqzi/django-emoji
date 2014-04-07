import os
import re

from django.contrib.staticfiles.storage import staticfiles_storage

try:
    from ._unicode_characters import UNICODE_ALIAS
except ImportError as exc:
    UNICODE_ALIAS = {}

from . import settings

__all__ = ('Emoji',)


class Emoji(object):
    """Test if an emoji exists in the library and returns the URL to it.
    Also can add emojis to a text if they match the pattern :emoticon:.

    Usage:
    >>> emoji = Emoji()
    >>> 'dog' in emoji
    True
    >>> 'doesntexistatall' in emoji
    False
    >>> emoji['dog']  # Uses staticfiles app internally
    '/static/emoji/img/dog.png'
    >>> emoji.replace("I am a :cat:.")
    'I am a <img src="/static/emoji/img/cat.png" alt="cat" class="emoji">.'

    This class is a singleton and if imported as following an instantiated
    version will be imported.
    >>> from emoji import Emoji
    >>> Emoji['dog']
    '/static/emoji/dog.png'

    """
    _static_path = 'emoji/img'
    _image_path = os.path.join(os.path.dirname(__file__),
                               'static', 'emoji', 'img')
    _instance = None
    _pattern = re.compile(r':([a-z0-9\+\-_]+):', re.I)
    _files = []
    _unicode_characters = UNICODE_ALIAS

    # This character acts as a modifier, if it's ever seen then remove
    # it because the modification is done when converting to an image
    # anyway.
    _unicode_modifiers = (u'\ufe0e', u'\ufe0f')

    # HTML entities regexs
    _html_entities_integer_unicode_regex = re.compile(r'&#([0-9]+);')
    _html_entities_hex_unicode_regex = re.compile(r'&#x([0-9a-f]+);', re.I)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Emoji, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.names()

    def __contains__(self, value):
        return value in self._files

    def keys(self):
        return self._files

    def __getitem__(self, item):
        if item in self._files:
            return self._static_url(item)

    def _static_url(self, name):
        return staticfiles_storage.url(
            '{0}/{1}.png'.format(self._static_path, name)
        )

    def _image_string(self, filename, alt=None):
        title = ' '.join(filename.split('_'))

        return settings.EMOJI_IMG_TAG.format(
            self._static_url(filename),
            alt or title,
            title,
        )

    @classmethod
    def names(cls):
        """A list of all emoji names without file extension."""
        if not cls._files:
            for f in os.listdir(cls._image_path):
                if(not f.startswith('.') and
                   os.path.isfile(os.path.join(cls._image_path, f))):
                    cls._files.append(os.path.splitext(f)[0])

        return cls._files

    @classmethod
    def replace(cls, replacement_string):
        """Add in valid emojis in a string where a valid emoji is between ::"""
        e = cls()

        def _replace_emoji(match):
            val = match.group(1)
            if val in e:
                return e._image_string(match.group(1))
            else:
                return match.group(0)

        return e._pattern.sub(_replace_emoji, replacement_string)

    @classmethod
    def replace_unicode(cls, replacement_string):
        """This method will iterate over every character in
        ``replacement_string`` and see if it mathces any of the
        unicode codepoints that we recognize. If it does then it will
        replace that codepoint with an image just like ``replace``.

        NOTE: This will only work with Python versions built with wide
        unicode caracter support. Python 3 should always work but
        Python 2 will have to tested before deploy.

        """
        e = cls()
        output = []
        prev = None

        if settings.EMOJI_REPLACE_HTML_ENTITIES:
            replacement_string = cls.replace_html_entities(replacement_string)

        for i, character in enumerate(replacement_string):
            if character in cls._unicode_modifiers:
                continue

            """check character is lead part of
            wide unicode emoji like u'\U0001f004'
            """
            if ord(character) == 55357:
                prev = character
                continue

            character = prev + character if prev else character
            prev = None

            name = e.name_for(character)
            if name:
                character = e._image_string(name, alt=character)

            output.append(character)

        return ''.join(output)

    @classmethod
    def name_for(cls, character):
        for modifier in cls._unicode_modifiers:
            character = character.replace(modifier, '')

        return cls._unicode_characters.get(character, False)

    @classmethod
    def replace_html_entities(cls, replacement_string):
        """Replaces HTML escaped unicode entities with their unicode
        equivalent. If the setting `EMOJI_REPLACE_HTML_ENTITIES` is
        `True` then this conversation will always be done in
        `replace_unicode` (default: True).

        """
        def _hex_to_unicode(hex_code):
            return ('\U'+ hex_code.rjust(8, '0')).decode('unicode-escape')

        def _replace_integer_entity(match):
            hex_val = hex(int(match.group(1)))

            return _hex_to_unicode(hex_val.replace('0x',''))

        def _replace_hex_entity(match):
            return _hex_to_unicode(match.group(1))

        # replace integer code points, &#65;
        replacement_string = re.sub(
            re._html_entities_integer_unicode_regex,
            _replace_integer_entity,
            replacement_string
        )
        # replace hex code points, &#x41;
        replacement_string = re.sub(
            self._html_entities_hex_unicode_regex,
            _replace_hex_entity,
            replacement_string
        )

        return replacement_string
