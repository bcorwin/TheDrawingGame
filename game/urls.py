from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
    url(r'^submit/$', views.image, name='submit_round'),
    url(r'(?P<code>.*)', views.show_round, name='show_round'),
)