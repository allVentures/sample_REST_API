from django.conf.urls import url
from django.contrib import admin

from movielist.views import MovieListView, MovieView
from showtimes.views import CinemaListView, CinemaView, ScreeningsListView, ScreeningView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^movies/$', MovieListView.as_view()),
    url(r'^movies/(?P<pk>[0-9]+)/$', MovieView.as_view()),
    url(r'^cinemas/$', CinemaListView.as_view()),
    url(r'^cinemas/(?P<pk>[0-9]+)/$', CinemaView.as_view()),
    url(r'^screens/$', ScreeningsListView.as_view()),
    url(r'^screens/(?P<pk>[0-9]+)/$', ScreeningView.as_view()),
]
