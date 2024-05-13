from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.registerUser, name="register"),
    path('profiles/', views.profiles, name="profiles"),
    path('profile/', views.userProfile, name="user-profile"),
    path('profile/<uuid:pk>/', views.adminUserProfile, name="admin-user-profile"),
    path('update_user/', views.update_user, name='update_user'),
]
