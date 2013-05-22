from django.views.generic import TemplateView
from emoji import Emoji


class EmojiTestReplaceTagView(TemplateView):
    template_name = 'emoji_list.html'

    def get_context_data(self, **kwargs):
        context = (super(EmojiTestReplaceTagView, self)
                   .get_context_data(**kwargs))
        limit = int(self.request.GET.get('limit', 0))
        emojis = []

        for i, emoji in enumerate(sorted(Emoji.keys())):
            if limit and i >= limit: break
            emojis.append(':{0}:'.format(emoji))

        context['emojis'] = emojis
        return context
