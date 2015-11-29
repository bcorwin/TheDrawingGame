from django.conf.urls import patterns, include, url
from django.contrib import admin
from game import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TheDrawingGame.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/', include('game.urls')),
    url(r'^view/(?P<code>.*)', views.view_game, name='view_game'),
    url(r'^$', views.home, name="home"),
)
