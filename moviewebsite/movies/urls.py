# movies/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('delete/<int:id>/',views.delete_movie, name='delete'),
    path('profile/', views.profile, name='profile'),
]
