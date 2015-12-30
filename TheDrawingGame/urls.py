from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from game import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wait/(?P<code>.*)', views.wait_round, name='wait_game'),
    url(r'^reset/(?P<code>.*)', views.reset_round, name='reset_game'),
    url(r'^game/', include('game.urls')),
    url(r'^howtoplay/', TemplateView.as_view(template_name='howtoplay.html')),
    url(r'^view/(?P<code>.*)', views.view_game, name='view_game'),
    url(r'^signup/(?P<code>.*)', views.signup, name='signup'),
    url(r'^$', views.home, name="home"),
)
