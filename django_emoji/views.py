import json

from django.http import HttpResponse
from django.views.generic import View

from . import Emoji


class EmojiJSONListView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps(dict(Emoji)),
                            content_type='application/json')
