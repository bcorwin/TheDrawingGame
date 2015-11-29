from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
    url(r'^view/(?P<code>.*)', views.view_game, name='view_game'),
    url(r'(?P<code>.*)', views.show_round, name='show_round'),
)