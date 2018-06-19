from django import template
from django.urls import reverse, NoReverseMatch
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe, SafeData
from django.utils.html import escape


from emoji import Emoji

register = template.Library()


@register.filter(name='emoji_replace', is_safe=True, needs_autoescape=True)
@stringfilter
def emoji_replace(value, autoescape=None):
    autoescape = autoescape and not isinstance(value, SafeData)
    if autoescape:
        value = escape(value)
    return mark_safe(Emoji.replace(value))


@register.filter(name='emoji_replace_unicode', is_safe=True,
                 needs_autoescape=True)
@stringfilter
def emoji_replace_unicode(value, autoescape=None):
    autoescape = autoescape and not isinstance(value, SafeData)
    if autoescape:
        value = escape(value)
    return mark_safe(Emoji.replace_unicode(value))


@register.filter(name='emoji_replace_html_entities',
                 is_safe=True, needs_autoescape=True)
@stringfilter
def emoji_replace_html_entities(value, autoescape=None):
    # Replaced before because it needs unescaped &
    value = Emoji.replace_html_entities(value)
    autoescape = autoescape and not isinstance(value, SafeData)
    if autoescape:
        value = escape(value)
    return mark_safe(value)


@register.simple_tag
def emoji_load():
    try:
        url = reverse('emoji:list.json')
    except NoReverseMatch:
        return ''
    else:
        return mark_safe("Emoji.setDataUrl('{0}').load();".format(url))
