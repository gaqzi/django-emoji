#!/usr/bin/env python
from pprint import pprint
import os
import sys
import unicodedata


# These are mapped to very generic characters (0-9 for instance) and
# shouldn't be replaced. Just skip them when adding
BLACKLIST = (
    'zero',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'hash',
    'copyright',
    'registered',
)

# These are modifier characters that changes the character before into
# another representation of itself, b&w/colored genereally.
# http://www.unicode.org/L2/L2011/11438-emoji-var.pdf
BLACKLIST_UNICODE = ('fe0f', 'fe0e')


def _convert_to_unicode(string):
    """This method should work with both Python 2 and 3 with the caveat
    that they need to be compiled with wide unicode character support.

    If there isn't wide unicode character support it'll blow up with a
    warning.

    """
    codepoints = []
    for character in string.split('-'):
        if character in BLACKLIST_UNICODE:
            next

        codepoints.append(
            '\U{0:0>8}'.format(character).decode('unicode-escape')
        )

    return codepoints


def create_list(image_path):
    unicode_characters = {}

    for f in os.listdir(image_path):
        name = os.path.splitext(f)[0]

        path = os.path.join(image_path, f)
        if os.path.islink(path) and not name in BLACKLIST:
            full_path = os.path.realpath(path)
            character = os.path.splitext(
                os.path.basename(full_path)
            )[0]

            for codepoint in _convert_to_unicode(character):
                unicode_characters[codepoint] = name

    return unicode_characters


if __name__ == '__main__':
    emojis = create_list('emoji/static/emoji/img/')
    if emojis:
        print '# This is an automatically generated file'
        print '# flake8:noqa'
        print ''
        sys.stdout.write('UNICODE_ALIAS = ')
        pprint(emojis, indent=4)
