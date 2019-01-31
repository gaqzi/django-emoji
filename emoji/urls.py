from django.conf.urls import url

from .views import EmojiJSONListView

app_name = "emoji"
urlpatterns = [
    url(r'^all.json$', EmojiJSONListView.as_view(), name='list.json'),
]
