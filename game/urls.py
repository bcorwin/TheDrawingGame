from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
    url(r'(?P<code>.*)', views.show_round, name='show_round'),
)