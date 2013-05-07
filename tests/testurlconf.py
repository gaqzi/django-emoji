from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'', include('emoji.urls', app_name='emoji', namespace='emoji')),
)
