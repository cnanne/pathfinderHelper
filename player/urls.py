from django.urls import path

from . import views

app_name = 'player'
urlpatterns = [
    path('', views.index, name='index'),
    path('skills', views.skills, name='skills'),
    path('addSkill', views.addSkill, name='addSkill'),
    path('skills/<str:skill_name>/', views.skillDetail, name='skillDetail'),
    path('<str:pc_name>', views.pcDetails,name='pcDetail'),
    path('<str:pc_name>/skillsAndSaves', views.skillsAndSaves, name='skillsAndSaves'),
    path('<str:pc_name>/inventory', views.inventory, name='inventory'),
]
