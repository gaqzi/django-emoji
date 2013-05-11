from django.conf.urls import patterns, url

from .views import EmojiJSONListView

urlpatterns = patterns('',
    url(r'^all.json$', EmojiJSONListView.as_view(), name='list.json'),
)
