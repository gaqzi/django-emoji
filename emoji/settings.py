from django.conf import settings

# The exact tag that is being used for replacing images and the values
# being passed in through `str#format`.
EMOJI_IMG_TAG = getattr(settings, 'EMOJI_IMG_TAG', (
    u'<img src="{0}" alt="{1}" title="{2}" class="emoji">'
))

EMOJI_ALT_AS_UNICODE = getattr(settings, 'EMOJI_ALT_AS_UNICODE', True)
EMOJI_REPLACE_HTML_ENTITIES = getattr(settings, 'EMOJI_REPLACE_HTML_ENTITIES',
                                      True)
