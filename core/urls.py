from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('api/skills/', views.skills_api, name='skills-api'),
    path('api/projects/', views.projects_api, name='projects-api'),
    path('api/publications/', views.publications_api, name='publications-api'),
]
