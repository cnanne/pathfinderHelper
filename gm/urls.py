from django.urls import path

from . import views

app_name = 'gm'
urlpatterns = [
    path('', views.index, name='index'),
    path('createPlayer', views.createPlayer, name='Create Player'),
    path('createPlayer/<int:part>', views.createPlayer, name='Create Player'),
    ]