from django.urls import path, re_path

from .views import EmojiJSONListView

app_name = "emoji"
urlpatterns = [
    re_path(r'^all.json$', EmojiJSONListView.as_view(), name='list.json'),
]
