from django.views.generic import TemplateView
from django_emoji import Emoji


class EmojiTestReplaceTagView(TemplateView):
    template_name = 'emoji_list.html'

    def get_context_data(self, **kwargs):
        context = (super(EmojiTestReplaceTagView, self)
                   .get_context_data(**kwargs))
        limit = int(self.request.GET.get('limit', 0))
        emojis = []

        for i, emoji in enumerate(sorted(Emoji.keys())):
            if limit and i >= limit:
                break
            emojis.append(':{0}:'.format(emoji))

        context['emojis'] = emojis
        return context


class EmojiTestReplcaceUnicodeTagView(TemplateView):
    template_name = 'emoji_replace_unicode.html'

    def get_context_data(self, **kwargs):
        context = (super(EmojiTestReplcaceUnicodeTagView, self)
                   .get_context_data(**kwargs))

        context['emoji'] = u'\U0001f48b'

        return context


class EmojiTestReplaceHtmlEntitiesView(TemplateView):
    template_name = 'emoji_replace_html_entities.html'

    def get_context_data(self, **kwargs):
        context = (super(EmojiTestReplaceHtmlEntitiesView, self)
                   .get_context_data(**kwargs))

        context['emoji_integer'] = '&#128139;'
        context['emoji_hex'] = '&#x0001f48b;'

        return context


class EmojiTestXSSFix(TemplateView):
    template_name = 'emoji_xss_fix.html'

    def get_context_data(self, **kwargs):
        context = (super(EmojiTestXSSFix, self)
                   .get_context_data(**kwargs))

        context['emoji_integer'] = '<em>&#128139;</em>'
        context['emoji_hex'] = '<em>&#x0001f48b;</em>'
        context['emoji_unicode'] = u'<em>\U0001f4a9<em>'
        context['emoji'] = '<em>:dog:</em>'

        return context
