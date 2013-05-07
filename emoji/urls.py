from django.conf.urls import patterns, url

from .views import EmojiListView

urlpatterns = patterns('',
    url(r'^all.json$', EmojiListView.as_view(), name='list'),
)
