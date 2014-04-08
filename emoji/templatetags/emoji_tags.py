from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


from emoji import Emoji

register = template.Library()


@register.filter(name='emoji_replace', is_safe=True)
@stringfilter
def emoji_replace(value):
    return mark_safe(Emoji.replace(value))


@register.filter(name='emoji_replace_unicode', is_safe=True)
@stringfilter
def emoji_replace_unicode(value):
    return mark_safe(Emoji.replace_unicode(value))


@register.filter(name='emoji_replace_html_entities', is_safe=True)
@stringfilter
def emoji_replace_html_entities(value):
    return mark_safe(Emoji.replace_html_entities(value))


@register.simple_tag
def emoji_load():
    try:
        url = reverse('emoji:list.json')
    except NoReverseMatch:
        return ''
    else:
        return "Emoji.setDataUrl('{0}').load();".format(url)
