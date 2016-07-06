# [v2.2 (2016-07-06)][release-2.2]

## features

* Support for Django 1.10 (beta but not expecting any breaking changes)

# v2.1 (2015-12-30)

* Support for Django 1.9

# v2.0 (2014-11-01)

## features

* Enable autoescaping for filters. This functions the same way as
  built-in Django filters work, which are enabled by default. Because
  this has the potential to break current installations the major has
  been bumped albeit being a small fix.


# v1.3 (2014-09-07)

## features

* Python 3 support
* test suite is now being run through tox for for all supported
  versions of Django and Python. 1.4 to 1.7 with their respective
  versions of Python.


# v1.2 (2014-04-09)

## features

* `Emoji.replace_html_entities` replaces all unicode html entities
  with their corresponding unicode character. This method is now by
  default called before `Emoji.replace_unicode`. (@pistos2)
* `Emoji.replace_unicode` will now set the `<img alt>` attribute to be
  the unicode character being replaced. This change done to allow
  marking and copying strings with emojis and the unicode character
  being copied along correctly. (@pistos2)
* Change the `<img>` tag to also have a title attribute that is the
  text representation of the current character being encoded.
* Added settings for new options:
  - `EMOJI_ALT_AS_UNICODE`, default: `True`
  - `EMOJI_REPLACE_HTML_ENTITIES`, default: `True`
  - `EMOJI_IMG_TAG`, default: 
       `<img src="{0}" alt="{1}" title="{2}" class="emoji">`
* Added support for running on a narrow unicode build of Python. 
  The test suite passed on narrow builds but it has not been production
  tested with a narrow build.
  

# v1.1 (2014-03-31)

## features

* `Emoji.name_for(unicode_character)` gives the name for a unicode character
* `Emoji.replace_unicode(unicode_string)` replaces all unicode emojis
  with images in the passed in string.

# v1.0 (2013-12-02)

* Initial public release

[release-2.2]: https://github.com/gaqzi/django-emoji/compare/v2.1.0...v2.2.0
