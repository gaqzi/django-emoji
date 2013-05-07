import os
import re

from django.contrib.staticfiles.storage import staticfiles_storage


class Emoji(object):
    ''' Test if an emoji exists in the library and returns the URL to it.
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
    '''
    _static_path = 'emoji/img'
    _image_path = os.path.join(os.path.dirname(__file__),
                               'static', 'emoji', 'img')
    _instance = None
    _pattern = re.compile(r':([a-z0-9\+\-_]+):', re.I)
    _files = []

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

    @classmethod
    def names(cls):
        ''' A list of all emoji names without file extension. '''
        if not cls._files:
            cls._files = map(lambda f: os.path.splitext(f)[0],
                             os.listdir(cls._image_path))

        return cls._files

    def _static_url(self, name):
        return staticfiles_storage.url(
            '{0}/{1}.png'.format(self._static_path, name)
        )

    @classmethod
    def replace(cls, replacement_string):
        '''Add in valid emojis in a string where a valid emoji is between ::'''
        e = cls()

        def _replace_emoji(match):
            val = match.group(1)
            if val in e:
                return '<img src="{0}" alt="{1}" class="emoji">'.format(
                    e._static_url(match.group(1)),
                    ' '.join(match.group(1).split('_'))
                )
            else:
                return match.group(0)

        return e._pattern.sub(_replace_emoji, replacement_string)
