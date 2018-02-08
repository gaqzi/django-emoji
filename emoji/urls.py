from django.urls import re_path

from .views import EmojiJSONListView

urlpatterns = [
    re_path(r'^all.json$', EmojiJSONListView.as_view(), name='list.json'),
]
