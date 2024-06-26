from django.urls import path
from . import views

app_name = 'projects'

urlpatterns =[
    path('', views.projects, name="projects"),
    path('project/<str:pk>/', views.project, name="project"),
    path('create-module/', views.createProject, name="create-project"),
    path('update-project/<str:pk>', views.updateProject, name="update-project"),
    path('delete-project/<str:pk>', views.deleteProject, name="delete-project"),
    path('create-lesson/', views.createLesson, name='create-lesson'),
    path('update_current_module/', views.update_current_module, name='update_current_module'),
]


