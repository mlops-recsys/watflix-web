from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('prefer/', views.preferenceTest, name='prefer-test'),
    path('preference/', views.preference, name='prefer'),
    path('movies/', views.recommendList, name='movies'),
    path('movies/list/', views.movieList, name='movie-list'),
]